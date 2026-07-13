import os
import re
import logging
import xml.etree.ElementTree as ET
from src.core.logger import nexus_logger

# Logger setup standard internal architecture rules
logger = logging.getLogger("ScatterXmlParser")

class ScatterXmlParser:
    def __init__(self, workspace_dir=None):
        # Android sandboxed path environment mapping support to prevent runtime crashes
        if workspace_dir is None:
            if 'ANDROID_ARGUMENT' in os.environ:
                from android.storage import app_storage_path
                self.workspace_dir = os.path.join(app_storage_path(), "workspace", "parsed")
            else:
                self.workspace_dir = "workspace/parsed"
        else:
            self.workspace_dir = workspace_dir
            
        self._ensure_workspace()

    def _ensure_workspace(self):
        """Parsing workspace directory structures ko initialize karti hai"""
        if not os.path.exists(self.workspace_dir):
            try:
                os.makedirs(self.workspace_dir)
            except Exception as e:
                nexus_logger.log_error(f"Parser workspace creation failure -> {str(e)}")

    def parse_file(self, file_path):
        """
        MediaTek standard Android txt scatter ya Unisoc XML layout config file ko auto-detect karke 
        partitions ka dictionary target data map generate karti hai.
        """
        if not os.path.exists(file_path):
            nexus_logger.log_error(f"Parser Core Mismatch: Configuration target absent at {file_path}")
            return None

        file_name = os.path.basename(file_path).lower()
        nexus_logger.log_info(f"Analyzing configuration structure node: {file_name}")

        try:
            # Auto-detection rule based on extensions or header structure
            if file_name.endswith('.xml'):
                return self._parse_unisoc_xml(file_path)
            elif file_name.endswith('.txt') or "scatter" in file_name:
                return self._parse_mediatek_txt(file_path)
            else:
                nexus_logger.log_error(f"Unsupported configuration format layout layout for file: {file_name}")
                return None
        except Exception as core_err:
            nexus_logger.log_error(f"Fatal processing error inside structural reflection pipeline -> {str(core_err)}")
            return None

    def _parse_mediatek_txt(self, file_path):
        """MediaTek traditional layout config text scatter lines parse karne ka algorithm"""
        nexus_logger.log_info("MediaTek structural layout target signature matched. Processing blocks...")
        partitions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Splitting configuration elements via standard block identifiers
            blocks = content.split('- partition_index:')
            total_blocks = len(blocks) - 1
            
            if total_blocks <= 0:
                # Fallback parser for older MTK scatter layouts (comma or space separated rules)
                return self._parse_old_mtk_format(content)

            for index, block in enumerate(blocks[1:], 1):
                part_info = {}
                
                # Dynamic matching regex block rules extraction logic
                name_match = re.search(r'partition_name:\s*(.*)', block)
                addr_match = re.search(r'linear_start_addr:\s*(.*)', block)
                size_match = re.search(r'physical_start_addr|partition_size:\s*(.*)', block)
                file_match = re.search(r'file_name:\s*(.*)', block)

                if name_match:
                    part_info['partition_label'] = name_match.group(1).strip()
                    part_info['linear_start_addr'] = addr_match.group(1).strip() if addr_match else "0x0000"
                    part_info['size_hex'] = size_match.group(1).strip() if size_match else "0x0000"
                    part_info['target_file'] = file_match.group(1).strip() if file_match else "NONE"
                    
                    partitions.append(part_info)
                
                # Synchronize data conversion processing states to active UI terminal interface
                nexus_logger.print_progress_bar(index, total_blocks, prefix='Parsing MTK Scatter')

            nexus_logger.log_info(f"MediaTek scatter translation mapping complete. Registered nodes: {len(partitions)}")
            return partitions
        except Exception as e:
            nexus_logger.log_error(f"MTK parsing pipeline broken: {str(e)}")
            return None

    def _parse_unisoc_xml(self, file_path):
        """Unisoc configuration XML schema elements parse karne ka dynamic logic block"""
        nexus_logger.log_info("Unisoc XML structural schema signature matched. Processing tags...")
        partitions = []

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find all partition tags dynamically inside the schema hierarchy
            part_nodes = root.findall('.//Partition') or root.findall('.//partition')
            total_elements = len(part_nodes)

            if total_elements == 0:
                # Fallback to general child loop search logic if tag attributes differ
                part_nodes = list(root.iter())
                total_elements = len(part_nodes)

            for index, node in enumerate(part_nodes, 1):
                attr = node.attrib
                if attr and ('name' in attr or 'id' in attr):
                    part_info = {
                        'partition_label': attr.get('name') or attr.get('id'),
                        'linear_start_addr': attr.get('address') or attr.get('start_addr') or "0x0000",
                        'size_hex': attr.get('size') or attr.get('length') or "0x0000",
                        'target_file': attr.get('file') or attr.get('image') or "NONE"
                    }
                    partitions.append(part_info)
                
                # Send tracking arrays stream sequence to UI
                nexus_logger.print_progress_bar(index, total_elements, prefix='Parsing Unisoc XML')

            nexus_logger.log_info(f"Unisoc layout schema translation complete. Registered nodes: {len(partitions)}")
            return partitions
        except Exception as xml_err:
            nexus_logger.log_error(f"XML structural processing loop interrupted -> {str(xml_err)}")
            return None

    def _parse_old_mtk_format(self, content):
        """Legacy system MTK configurations processing module fallback block"""
        partitions = []
        lines = content.splitlines()
        for line in lines:
            if line.startswith("MTK_") or "," in line:
                parts = line.split()
                if len(parts) >= 3:
                    partitions.append({
                        'partition_label': parts[0].strip(),
                        'linear_start_addr': parts[1].strip(),
                        'size_hex': parts[2].strip(),
                        'target_file': "NONE"
                    })
        return partitions

if __name__ == "__main__":
    parser = ScatterXmlParser()
    nexus_logger.log_info("Local Structural Scatter/XML Unit Verification Layer Operational.")
