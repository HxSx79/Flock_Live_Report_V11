import pandas as pd
import os
from typing import Dict

class BOMReader:
    def __init__(self, bom_file: str = "BOM.xlsx"):
        self.bom_file = bom_file
        self.bom_data = None
        self._load_bom()

    def _load_bom(self) -> None:
        """Load BOM data from Excel file"""
        if not os.path.exists(self.bom_file):
            print(f"Warning: BOM file not found: {self.bom_file}")
            self.bom_data = pd.DataFrame(columns=['Class_Name', 'Program', 'Part_Number', 'Part_Description'])
        else:
            try:
                self.bom_data = pd.read_excel(self.bom_file)
                print(f"Successfully loaded BOM with {len(self.bom_data)} entries")
            except Exception as e:
                print(f"Error loading BOM: {e}")
                self.bom_data = pd.DataFrame(columns=['Class_Name', 'Program', 'Part_Number', 'Part_Description'])

    def get_part_info(self, class_name: str) -> Dict[str, str]:
        """Get part information for a given class name"""
        if self.bom_data is None:
            return self._get_unknown_part_info()

        try:
            # Find matching row in BOM
            matching_row = self.bom_data[self.bom_data['Class_Name'] == class_name]
            
            if not matching_row.empty:
                row = matching_row.iloc[0]
                return {
                    'program': str(row['Program']),
                    'part_number': str(row['Part_Number']),
                    'description': str(row['Part_Description'])
                }
            else:
                print(f"Class name not found in BOM: {class_name}")
                return self._get_unknown_part_info()
                
        except Exception as e:
            print(f"Error retrieving part info: {e}")
            return self._get_unknown_part_info()

    def _get_unknown_part_info(self) -> Dict[str, str]:
        """Return default values for unknown parts"""
        return {
            'program': 'Unknown',
            'part_number': 'Unknown',
            'description': 'Unknown'
        }