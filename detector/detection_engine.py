import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from scipy import stats
import json
from typing import Dict, List, Tuple, Any
import logging
from .config import config

logger = logging.getLogger(__name__)

class DataPoisonDetector:
    """
    Advanced Data Poison Detection System
    
    Implements multiple anomaly detection methods:
    - Z-Score (statistical outlier detection)
    - IQR (Interquartile Range method)
    - Isolation Forest (machine learning)
    - One-Class SVM (machine learning)
    
    Processes data in distributed chunks to simulate multiple servers.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.config = config
        
    def detect_numeric_columns(self, df: pd.DataFrame) -> List[str]:
        """Automatically detect numeric columns in the dataset"""
        numeric_columns = []
        for col in df.columns:
            # Try to convert to numeric, ignore errors
            try:
                pd.to_numeric(df[col], errors='raise')
                numeric_columns.append(col)
            except (ValueError, TypeError):
                continue
        return numeric_columns
    
    def split_data_into_chunks(self, df: pd.DataFrame, num_chunks: int = None) -> List[pd.DataFrame]:
        """Split data into chunks for distributed processing"""
        if num_chunks is None:
            num_chunks = self.config.get('distributed_chunks', 3)
        
        chunk_size = len(df) // num_chunks
        chunks = []
        
        for i in range(num_chunks):
            start_idx = i * chunk_size
            if i == num_chunks - 1:  # Last chunk gets remaining rows
                end_idx = len(df)
            else:
                end_idx = (i + 1) * chunk_size
            chunks.append(df.iloc[start_idx:end_idx].copy())
        
        return chunks
    
    def z_score_detection(self, df: pd.DataFrame, numeric_cols: List[str], threshold: float = None) -> Dict[int, bool]:
        """
        Z-Score based anomaly detection
        Flags rows where any numeric column has |Z-score| > threshold
        Very conservative threshold for cleaner detection
        """
        if threshold is None:
            threshold = self.config.get('z_score_threshold', 4.0)
        
        flagged_rows = {}
        
        for col in numeric_cols:
            # Calculate Z-scores
            z_scores = np.abs(stats.zscore(df[col], nan_policy='omit'))
            
            # Find rows where Z-score exceeds threshold
            outlier_indices = np.where(z_scores > threshold)[0]
            
            for idx in outlier_indices:
                global_idx = df.index[idx]
                flagged_rows[global_idx] = True
        
        return flagged_rows
    
    def iqr_detection(self, df: pd.DataFrame, numeric_cols: List[str], multiplier: float = None) -> Dict[int, bool]:
        """
        Interquartile Range (IQR) based anomaly detection
        Flags rows where any numeric column value is outside [Q1 - multiplier*IQR, Q3 + multiplier*IQR]
        Very conservative multiplier for cleaner detection
        """
        if multiplier is None:
            multiplier = self.config.get('iqr_multiplier', 2.5)
        
        flagged_rows = {}
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Configurable bounds
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            
            # Find outliers
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            for idx in outliers.index:
                flagged_rows[idx] = True
        
        return flagged_rows
    
    def isolation_forest_detection(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict[int, bool]:
        """
        Isolation Forest based anomaly detection
        Uses machine learning to identify anomalies
        """
        flagged_rows = {}
        
        if len(numeric_cols) == 0:
            return flagged_rows
        
        # Prepare data for ML models
        X = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        # Adaptive contamination based on dataset size
        # Very conservative settings for clean datasets
        dataset_size = len(df)
        contamination = self.config.get_adaptive_contamination(dataset_size)
        
        # Create a new Isolation Forest with adaptive contamination
        isolation_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        
        # Fit and predict
        predictions = isolation_forest.fit_predict(X)
        
        # -1 indicates anomaly, 1 indicates normal
        anomaly_indices = np.where(predictions == -1)[0]
        
        for idx in anomaly_indices:
            global_idx = df.index[idx]
            flagged_rows[global_idx] = True
        
        return flagged_rows
    
    def one_class_svm_detection(self, df: pd.DataFrame, numeric_cols: List[str]) -> Dict[int, bool]:
        """
        One-Class SVM based anomaly detection
        Uses support vector machine to identify anomalies
        """
        flagged_rows = {}
        
        if len(numeric_cols) == 0:
            return flagged_rows
        
        # Prepare data for ML models
        X = df[numeric_cols].fillna(df[numeric_cols].mean())
        
        # Standardize the data
        X_scaled = self.scaler.fit_transform(X)
        
        # Adaptive nu parameter based on dataset size
        # Very conservative settings for clean datasets
        dataset_size = len(df)
        nu = self.config.get_adaptive_nu(dataset_size)
        
        # Create a new One-Class SVM with adaptive nu
        one_class_svm = OneClassSVM(
            kernel='rbf',
            nu=nu,
            gamma='scale'
        )
        
        # Fit and predict
        predictions = one_class_svm.fit_predict(X_scaled)
        
        # -1 indicates anomaly, 1 indicates normal
        anomaly_indices = np.where(predictions == -1)[0]
        
        for idx in anomaly_indices:
            global_idx = df.index[idx]
            flagged_rows[global_idx] = True
        
        return flagged_rows
    
    def process_chunk(self, chunk: pd.DataFrame, chunk_id: int) -> Dict[str, Any]:
        """
        Process a single chunk of data using all detection methods
        Returns results for this chunk
        """
        logger.info(f"Processing chunk {chunk_id} with {len(chunk)} rows")
        
        # Detect numeric columns
        numeric_cols = self.detect_numeric_columns(chunk)
        
        if len(numeric_cols) == 0:
            return {
                'chunk_id': chunk_id,
                'error': 'No numeric columns found in the dataset',
                'flagged_rows': {},
                'method_results': {}
            }
        
        # Apply all detection methods
        z_score_results = self.z_score_detection(chunk, numeric_cols)
        iqr_results = self.iqr_detection(chunk, numeric_cols)
        isolation_forest_results = self.isolation_forest_detection(chunk, numeric_cols)
        one_class_svm_results = self.one_class_svm_detection(chunk, numeric_cols)
        
        # Combine results - require at least 2 methods to flag a row for it to be considered poisoned
        method_flags = {}
        for row_idx in z_score_results.keys():
            method_flags[row_idx] = method_flags.get(row_idx, 0) + 1
        for row_idx in iqr_results.keys():
            method_flags[row_idx] = method_flags.get(row_idx, 0) + 1
        for row_idx in isolation_forest_results.keys():
            method_flags[row_idx] = method_flags.get(row_idx, 0) + 1
        for row_idx in one_class_svm_results.keys():
            method_flags[row_idx] = method_flags.get(row_idx, 0) + 1
        
        # Only flag rows that are detected by at least consensus_threshold methods
        consensus_threshold = self.config.get('consensus_threshold', 2)
        all_flagged_rows = {row_idx for row_idx, count in method_flags.items() if count >= consensus_threshold}
        
        # Create detailed results
        method_results = {
            'z_score': {
                'flagged_count': len(z_score_results),
                'flagged_rows': list(z_score_results.keys())
            },
            'iqr': {
                'flagged_count': len(iqr_results),
                'flagged_rows': list(iqr_results.keys())
            },
            'isolation_forest': {
                'flagged_count': len(isolation_forest_results),
                'flagged_rows': list(isolation_forest_results.keys())
            },
            'one_class_svm': {
                'flagged_count': len(one_class_svm_results),
                'flagged_rows': list(one_class_svm_results.keys())
            }
        }
        
        return {
            'chunk_id': chunk_id,
            'numeric_columns': numeric_cols,
            'total_rows': len(chunk),
            'flagged_rows': list(all_flagged_rows),
            'flagged_count': len(all_flagged_rows),
            'method_results': method_results
        }
    
    def detect_poisoned_data(self, file_path: str, use_lenient_mode: bool = False) -> Dict[str, Any]:
        """
        Main method to detect poisoned data in a file (CSV or Excel)
        
        Args:
            file_path: Path to the file (CSV, XLSX, or XLS)
            
        Returns:
            Dictionary containing detection results
        """
        try:
            # Load the file based on extension
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'csv':
                df = pd.read_csv(file_path)
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            logger.info(f"Loaded {file_extension.upper()} file with {len(df)} rows and {len(df.columns)} columns")
            
            # Split data into chunks for distributed processing
            chunks = self.split_data_into_chunks(df, num_chunks=3)
            logger.info(f"Split data into {len(chunks)} chunks")
            
            # Process each chunk
            chunk_results = []
            total_flagged_rows = set()
            all_method_results = {
                'z_score': {'flagged_count': 0, 'flagged_rows': []},
                'iqr': {'flagged_count': 0, 'flagged_rows': []},
                'isolation_forest': {'flagged_count': 0, 'flagged_rows': []},
                'one_class_svm': {'flagged_count': 0, 'flagged_rows': []}
            }
            
            # Adjust thresholds if lenient mode is enabled (for pre-cleaned datasets)
            if use_lenient_mode:
                # Store original values
                original_z = self.config.get('z_score_threshold', 4.0)
                original_iqr = self.config.get('iqr_multiplier', 2.5)
                original_consensus = self.config.get('consensus_threshold', 2)
                
                # Temporarily use more lenient thresholds
                self.config.config['z_score_threshold'] = original_z + 2.0  # Increase by 2
                self.config.config['iqr_multiplier'] = original_iqr + 1.0   # Increase by 1
                self.config.config['consensus_threshold'] = min(original_consensus + 1, 4)  # Require more consensus
            
            for i, chunk in enumerate(chunks):
                chunk_result = self.process_chunk(chunk, i)
                chunk_results.append(chunk_result)
                
                # Aggregate results across chunks
                total_flagged_rows.update(chunk_result['flagged_rows'])
                
                # Aggregate method results
                for method, results in chunk_result['method_results'].items():
                    all_method_results[method]['flagged_count'] += results['flagged_count']
                    all_method_results[method]['flagged_rows'].extend(results['flagged_rows'])
            
            # Restore original thresholds if lenient mode was used
            if use_lenient_mode:
                self.config.config['z_score_threshold'] = original_z
                self.config.config['iqr_multiplier'] = original_iqr
                self.config.config['consensus_threshold'] = original_consensus
            
            # Create detailed row-level results
            row_results = []
            for idx, row in df.iterrows():
                is_flagged = idx in total_flagged_rows
                
                # Determine which methods flagged this row
                z_score_flag = idx in all_method_results['z_score']['flagged_rows']
                iqr_flag = idx in all_method_results['iqr']['flagged_rows']
                isolation_forest_flag = idx in all_method_results['isolation_forest']['flagged_rows']
                one_class_svm_flag = idx in all_method_results['one_class_svm']['flagged_rows']
                
                row_results.append({
                    'row_index': idx,
                    'is_flagged': is_flagged,
                    'z_score_flag': z_score_flag,
                    'iqr_flag': iqr_flag,
                    'isolation_forest_flag': isolation_forest_flag,
                    'one_class_svm_flag': one_class_svm_flag,
                    'row_data': row.to_dict()
                })
            
            # Calculate summary statistics
            total_rows = len(df)
            flagged_count = len(total_flagged_rows)
            clean_count = total_rows - flagged_count
            
            # Create final results
            results = {
                'success': True,
                'total_rows': total_rows,
                'flagged_rows': flagged_count,
                'clean_rows': clean_count,
                'detection_rate': (flagged_count / total_rows * 100) if total_rows > 0 else 0,
                'method_summary': all_method_results,
                'row_results': row_results,
                'chunk_results': chunk_results,
                'numeric_columns': chunk_results[0].get('numeric_columns', []) if chunk_results else []
            }
            
            logger.info(f"Detection completed: {flagged_count}/{total_rows} rows flagged as poisoned")
            return results
            
        except Exception as e:
            logger.error(f"Error during detection: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'total_rows': 0,
                'flagged_rows': 0,
                'clean_rows': 0,
                'detection_rate': 0,
                'method_summary': {},
                'row_results': [],
                'chunk_results': [],
                'numeric_columns': []
            } 