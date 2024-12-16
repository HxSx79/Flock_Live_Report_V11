import cv2
from typing import Dict, List, Set, Optional
from .geometry import Point
from .tracking import TrackingState

class LineCounter:
    def __init__(self):
        self.counted_ids: Set[int] = set()
        self.line_x_position = 0.5  # Vertical line at 50% of width
        self.line_y_position = 0.5  # Horizontal line at 50% of height
        self.tracking_state = TrackingState()
        self.counts = {'line1': 0, 'line2': 0}
        self.latest_crossings = {'line1': None, 'line2': None}
        self.frame_width = 0
        self.frame_height = 0

    def update_frame_dimensions(self, width: int, height: int) -> None:
        """Update frame dimensions"""
        self.frame_width = width
        self.frame_height = height
        self.tracking_state.update_frame_dimensions(width, height)

    def update_counts(self, detections: List[Dict]) -> None:
        """Update part counts based on detected objects crossing the line"""
        if not detections or self.frame_width == 0 or self.frame_height == 0:
            return

        for detection in detections:
            track_id = detection['track_id']
            current_pos = Point(detection['center'][0], detection['center'][1])
            
            if self.tracking_state.has_previous_position(track_id):
                prev_pos = self.tracking_state.get_previous_position(track_id)
                if self._has_crossed_line(prev_pos, current_pos):
                    self._process_line_crossing(track_id, detection, current_pos)
            
            self.tracking_state.update_position(track_id, current_pos)

    def _has_crossed_line(self, prev_pos: Point, current_pos: Point) -> bool:
        """Check if movement between points crosses the vertical counting line"""
        line_x = int(self.frame_width * self.line_x_position)
        
        # Check if crossed from left to right or right to left
        crossed_left_to_right = prev_pos.x < line_x and current_pos.x >= line_x
        crossed_right_to_left = prev_pos.x > line_x and current_pos.x <= line_x
        
        if crossed_left_to_right or crossed_right_to_left:
            print(f"Line crossing detected at position ({current_pos.x}, {current_pos.y})")
            return True
        return False

    def _process_line_crossing(self, track_id: int, detection: Dict, position: Point) -> None:
        """Process a line crossing event"""
        if track_id not in self.counted_ids:
            # Calculate actual line y-position
            line_y = int(self.frame_height * self.line_y_position)
            
            # Determine which line based on y-position relative to horizontal line
            line_key = 'line1' if position.y < line_y else 'line2'
            
            # Update counts and store crossing information
            self.counts[line_key] += 1
            self.latest_crossings[line_key] = {
                'class_name': detection['class_name'],
                'timestamp': cv2.getTickCount()
            }
            
            print(f"Counted object for {line_key}: {detection['class_name']}")
            print(f"New count for {line_key}: {self.counts[line_key]}")
            self.counted_ids.add(track_id)

    def get_counts(self) -> Dict[str, int]:
        """Get current counts for both lines"""
        return self.counts.copy()

    def get_latest_crossings(self) -> Dict[str, Optional[Dict]]:
        """Get information about the latest crossings for each line"""
        return self.latest_crossings.copy()

    def reset(self) -> None:
        """Reset all counting data"""
        self.counted_ids.clear()
        self.tracking_state.reset()
        self.counts = {'line1': 0, 'line2': 0}
        self.latest_crossings = {'line1': None, 'line2': None}