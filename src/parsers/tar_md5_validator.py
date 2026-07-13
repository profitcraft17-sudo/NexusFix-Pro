import os
import tarfile
import hashlib
import logging
from src.core.logger import nexus_logger

# Logger setup standard internal architecture rules
logger = logging.getLogger("TarMd5Validator")

class TarMd5Validator:
    def __init__(self, workspace_dir=None):
        # FIXED: Android sandboxed path environment mapping support added to prevent directory creation failure
        if workspace_dir is None:
            if 'ANDROID_ARGUMENT' in os.environ:
                from android.storage import app_storage_path
                self.workspace_dir = os.path.join(app_storage_path(), "workspace", "extracted")
            else:
                self.workspace_dir = "workspace/extracted"
        else:
            self.workspace_dir = workspace_dir
            
        self._ensure_workspace()

    def _ensure_workspace(self):
        """Extraction workspace directory structure paths check karke initialize karti hai"""
        if not os.path.exists(self.workspace_dir):
            try:
                os.makedirs(self.workspace_dir)
            except Exception as e:
                nexus_logger.log_error(f"Workspace creation failure context trace -> {str(e)}")

    def validate_md5(self, file_path):
        """Samsung standard firmware `.tar.md5` ke footer hash checksum structure ko deep verify karti hai"""
        if not os.path.exists(file_path):
            nexus_logger.log_error(f"Parser Target Missing: File not found at {file_path}")
            return False
        if not file_path.endswith('.md5'):
            nexus_logger.log_info("Standard TAR archive detected. Skipping explicit MD5 hash matching block.")
            return True
        nexus_logger.log_info(f"Initializing MD5 integrity check for: {os.path.basename(file_path)}")
                
        try:
            file_size = os.path.getsize(file_path)
            # Samsung footer typically contains spaces, newlines, and "MD5sum: [32 chars hex]"
            # So reading last 64 bytes safely encapsulates this segment
            footer_buffer_size = min(64, file_size)
                        
            with open(file_path, 'rb') as f:
                f.seek(-footer_buffer_size, os.SEEK_END)
                footer_data = f.read().decode('utf-8', errors='ignore').strip()
            
            # Footer se explicit 32-character hex hash extract karna
            stored_hash = None
            if "MD5sum:" in footer_data:
                parts = footer_data.split("MD5sum:")
                if len(parts) > 1:
                    stored_hash = parts[1].strip().split()[0] # Clear extra whitespace
            
            if not stored_hash or len(stored_hash) != 32:
                # Fallback if custom packing drops the token string prefix
                stored_hash = footer_data[-32:]
            
            # FIXED: Fixed TypeError crash by searching plain string token instead of byte string in string context
            target_token = "md5sum:"
            token_index = footer_data.lower().find(target_token)
            
            payload_bound = file_size - (footer_buffer_size - token_index) if token_index != -1 else file_size - 45
            
            if payload_bound <= 0 or len(stored_hash) != 32:
                # Hard fallback logic matching generic boundaries
                payload_bound = file_size - 45 

            md5_generator = hashlib.md5()
            bytes_processed = 0
            chunk_size = 2 * 1024 * 1024  # 2MB dynamic buffer for higher processing speed
                        
            with open(file_path, 'rb') as f:
                while bytes_processed < payload_bound:
                    to_read = min(chunk_size, payload_bound - bytes_processed)
                    chunk = f.read(to_read)
                    if not chunk:
                        break
                    md5_generator.update(chunk)
                    bytes_processed += len(chunk)
                                        
                    # Update live progress bar state via core engine link
                    nexus_logger.print_progress_bar(bytes_processed, payload_bound, prefix='Analyzing Checksum')
            
            calculated_hash = md5_generator.hexdigest().strip()
                        
            if calculated_hash.lower() == stored_hash.lower():
                nexus_logger.log_info("MD5 Verification SUCCESS. Integrity checksum matches master firmware.")
                return True
            else:
                nexus_logger.log_error(f"MD5 CORRUPTED! Stored: {stored_hash} | Computed: {calculated_hash}")
                return False
        except Exception as err:
            nexus_logger.log_error(f"Fatal exception hit during data stream parsing -> {str(err)}")
            return False

    def extract_tar(self, file_path):
        """Firmware images block ko extract karke partition image matrix nodes ready karti hai"""
        if not self.validate_md5(file_path):
            nexus_logger.log_error("TAR extraction aborted due to initial validation layout failure.")
            return None
        extracted_files = []
        nexus_logger.log_info(f"Extracting firmware partition layers into target storage pipeline...")
                
        try:
            with tarfile.open(file_path, 'r:*') as tar:
                # Security feature check for safe extraction (Path Traversal Guard)
                if hasattr(tar, 'data_filter'):
                    tar.extraction_filter = getattr(tar, 'data_filter')
                members = tar.getmembers()
                total_files = len(members)
                                
                for index, member in enumerate(members, 1):
                    # Path traversal sanitization fallback guard check
                    clean_name = os.path.basename(member.name)
                    if not clean_name or member.name.startswith(("/", "..")):
                        continue
                                            
                    nexus_logger.log_debug(f"Extracting sub-layer block target node: {clean_name}")
                    tar.extract(member, path=self.workspace_dir)
                    target_out_path = os.path.join(self.workspace_dir, member.name)
                    extracted_files.append(target_out_path)
                                        
                    # Updating global dashboard tracker progress status indicators
                    nexus_logger.print_progress_bar(index, total_files, prefix='Extracting Archive')
                                
                nexus_logger.log_info(f"Archive structure unrolled completely. Total components parsed: {len(extracted_files)}")
            return extracted_files
        except Exception as tar_err:
            nexus_logger.log_error(f"TAR tracking extraction system failure -> {str(tar_err)}")
            return None

if __name__ == "__main__":
    validator = TarMd5Validator()
    nexus_logger.log_info("Local Parser Unit Verification Layer Ready.")
