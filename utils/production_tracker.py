from datetime import datetime
from typing import Dict, Optional
from .bom_reader import BOMReader
from .excel_logger import ExcelLogger

class ProductionTracker:
    def __init__(self):
        self.bom_reader = BOMReader()
        self.excel_logger = ExcelLogger()
        self.line_data = {
            'line1': {
                'part': {'program': 'No Part', 'number': 'No Part', 'description': 'No Part'},
                'production': {'quantity': 0, 'delta': 0},
                'scrap': {'total': 0, 'rate': 0}
            },
            'line2': {
                'part': {'program': 'No Part', 'number': 'No Part', 'description': 'No Part'},
                'production': {'quantity': 0, 'delta': 0},
                'scrap': {'total': 0, 'rate': 0}
            }
        }
        self.processed_timestamps = set()
        self.total_quantity = 0
        self.total_scrap = 0

    def update_production(self, counts: Dict[str, int], latest_crossings: Dict[str, Optional[Dict]]) -> None:
        """Update production data based on line crossings"""
        for line_key in ['line1', 'line2']:
            # Calculate delta before updating quantity
            old_quantity = self.line_data[line_key]['production']['quantity']
            new_quantity = counts[line_key]
            delta = new_quantity - old_quantity
            
            # Update counts and delta
            self.line_data[line_key]['production']['quantity'] = new_quantity
            self.line_data[line_key]['production']['delta'] = delta
            
            # Update total quantity if there's a new crossing
            if delta > 0:
                self.total_quantity += delta
            
            # Process new crossings
            crossing_data = latest_crossings[line_key]
            if crossing_data:
                timestamp = crossing_data['timestamp']
                class_name = crossing_data['class_name']
                
                # Always update part info for the latest detection
                print(f"Processing crossing for {line_key}: {class_name}")
                
                # Get part info from BOM
                part_info = self.bom_reader.get_part_info(class_name)
                
                # Update line data with the latest part information
                self.line_data[line_key]['part'].update({
                    'program': part_info['program'],
                    'number': part_info['part_number'],
                    'description': part_info['description']
                })
                
                # Only log to Excel if it's a new crossing
                if timestamp not in self.processed_timestamps:
                    self.excel_logger.log_crossing(
                        line_number=1 if line_key == 'line1' else 2,
                        class_name=class_name,
                        part_info=part_info
                    )
                    self.processed_timestamps.add(timestamp)
                    print(f"Logged new crossing for {line_key}")

            # Update scrap rate
            total_parts = self.line_data[line_key]['production']['quantity']
            scrap_total = self.line_data[line_key]['scrap']['total']
            if total_parts > 0:
                scrap_rate = (scrap_total / total_parts) * 100
                self.line_data[line_key]['scrap']['rate'] = round(scrap_rate, 1)

    def get_all_data(self) -> Dict:
        """Get all production data for display"""
        # Calculate total scrap and average scrap rate
        total_scrap = (self.line_data['line1']['scrap']['total'] + 
                      self.line_data['line2']['scrap']['total'])
        
        total_parts = self.total_quantity
        avg_scrap_rate = 0
        if total_parts > 0:
            avg_scrap_rate = round((total_scrap / total_parts) * 100, 1)

        return {
            'line1_part': self.line_data['line1']['part'],
            'line1_production': self.line_data['line1']['production'],
            'line1_scrap': self.line_data['line1']['scrap'],
            'line2_part': self.line_data['line2']['part'],
            'line2_production': self.line_data['line2']['production'],
            'line2_scrap': self.line_data['line2']['scrap'],
            'total_quantity': self.total_quantity,
            'total_delta': (self.line_data['line1']['production']['delta'] + 
                          self.line_data['line2']['production']['delta']),
            'total_scrap': total_scrap,
            'average_scrap_rate': avg_scrap_rate
        }