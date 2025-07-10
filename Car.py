import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

class SelfDrivingCarSimulator:
    def __init__(self):
        # Initialize simulation parameters
        self.car_pos = np.array([0.0, 0.0])
        self.car_angle = 0.0
        self.speed = 0.0
        self.max_speed = 3.0
        self.acceleration = 0.1
        self.steering_sensitivity = 0.05
        
        # Create road with lanes
        self.road_length = 100
        self.lane_width = 3.5
        self.lanes = 3
        self.road_center = 0
        
        # Add obstacles
        self.obstacles = [
            {"pos": np.array([20, self.lane_width]), "radius": 1.5},
            {"pos": np.array([40, -self.lane_width]), "radius": 1.5},
            {"pos": np.array([60, 0]), "radius": 1.5}
        ]
        
        # Traffic light
        self.traffic_light_pos = 80
        self.traffic_light_state = "green"  # "green", "yellow", "red"
        self.light_timer = 0
        
        # Generate reference path (center lane)
        self.reference_path = []
        for x in np.arange(0, self.road_length, 1):
            self.reference_path.append(np.array([x, self.road_center]))
        
        # Initialize plot
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        
    def update_traffic_light(self):
        """Cycle through traffic light states"""
        self.light_timer += 1
        if self.light_timer > 100:
            if self.traffic_light_state == "green":
                self.traffic_light_state = "yellow"
            elif self.traffic_light_state == "yellow":
                self.traffic_light_state = "red"
            else:
                self.traffic_light_state = "green"
            self.light_timer = 0
    
    def perception(self):
        """Simulate sensor inputs"""
        detected_objects = []
        
        # Detect obstacles
        for obs in self.obstacles:
            dist = np.linalg.norm(obs["pos"] - self.car_pos)
            if dist < 20:  # Sensor range
                detected_objects.append({
                    "type": "obstacle",
                    "position": obs["pos"],
                    "radius": obs["radius"],
                    "distance": dist
                })
        
        # Detect traffic light
        if (self.traffic_light_pos - 5 < self.car_pos[0] < self.traffic_light_pos + 5 and 
            abs(self.car_pos[1]) < self.lane_width * 1.5):
            detected_objects.append({
                "type": "traffic_light",
                "position": np.array([self.traffic_light_pos, self.lane_width * 2]),
                "state": self.traffic_light_state,
                "distance": abs(self.traffic_light_pos - self.car_pos[0])
            })
        
        return detected_objects
    
    def plan(self, detected_objects):
        """Determine target path based on environment"""
        target_path = self.reference_path.copy()
        current_lane = round(self.car_pos[1] / self.lane_width)
        
        # Check for obstacles in current lane
        for obj in detected_objects:
            if obj["type"] == "obstacle" and abs(obj["position"][1] - self.car_pos[1]) < self.lane_width/2:
                if 0 < obj["position"][0] - self.car_pos[0] < 30:  # Obstacle ahead
                    # Suggest lane change
                    if current_lane < self.lanes - 1:
                        # Move to right lane
                        for i, point in enumerate(target_path):
                            if point[0] > self.car_pos[0]:
                                target_path[i][1] = (current_lane + 1) * self.lane_width
                    elif current_lane > -self.lanes + 1:
                        # Move to left lane
                        for i, point in enumerate(target_path):
                            if point[0] > self.car_pos[0]:
                                target_path[i][1] = (current_lane - 1) * self.lane_width
            
            # Handle traffic light
            elif obj["type"] == "traffic_light" and obj["state"] in ["red", "yellow"]:
                if 0 < obj["position"][0] - self.car_pos[0] < 30:
                    # Slow down for traffic light
                    self.max_speed = 1.0
                if 0 < obj["position"][0] - self.car_pos[0] < 10:
                    # Stop for red light
                    if obj["state"] == "red":
                        self.max_speed = 0
        
        return target_path
    
    def control(self, target_path):
        """Control the vehicle to follow the path"""
        # Find the nearest point on the path ahead of the car
        lookahead_distance = 5 + self.speed * 2
        target_point = None
        
        for point in target_path:
            if point[0] > self.car_pos[0]:
                dist = np.linalg.norm(point - self.car_pos)
                if dist > lookahead_distance:
                    target_point = point
                    break
        
        if target_point is None:
            target_point = target_path[-1]
        
        # Calculate steering angle
        target_vector = target_point - self.car_pos
        desired_angle = np.arctan2(target_vector[1], target_vector[0])
        angle_error = (desired_angle - self.car_angle + np.pi) % (2 * np.pi) - np.pi
        
        # Adjust steering
        self.car_angle += angle_error * self.steering_sensitivity
        
        # Adjust speed
        if self.speed < self.max_speed:
            self.speed = min(self.speed + self.acceleration * 0.1, self.max_speed)
        else:
            self.speed = max(self.speed - self.acceleration * 0.1, self.max_speed)
        
        # Update position
        self.car_pos[0] += self.speed * np.cos(self.car_angle) * 0.1
        self.car_pos[1] += self.speed * np.sin(self.car_angle) * 0.1
    
    def update(self, frame):
        """Update simulation for each frame"""
        self.ax.clear()
        
        # Update traffic light
        self.update_traffic_light()
        
        # Run autonomous systems
        detected_objects = self.perception()
        target_path = self.plan(detected_objects)
        self.control(target_path)
        
        # Draw road
        for i in range(-self.lanes, self.lanes + 1):
            lane_pos = i * self.lane_width
            self.ax.plot([0, self.road_length], [lane_pos, lane_pos], 
                        'k--' if i != 0 else 'k-', linewidth=1 if i !=0 else 2)
        
        # Draw obstacles
        for obs in self.obstacles:
            circle = plt.Circle(obs["pos"], obs["radius"], color='red', alpha=0.5)
            self.ax.add_patch(circle)
        
        # Draw traffic light
        light_color = {'red': 'r', 'yellow': 'y', 'green': 'g'}[self.traffic_light_state]
        self.ax.add_patch(plt.Rectangle(
            (self.traffic_light_pos - 0.5, self.lane_width * 2), 
            1, 2, color='black'))
        self.ax.add_patch(plt.Circle(
            (self.traffic_light_pos, self.lane_width * 2 + 1.5), 
            0.4, color=light_color))
        
        # Draw path
        path_x = [p[0] for p in target_path]
        path_y = [p[1] for p in target_path]
        self.ax.plot(path_x, path_y, 'b-', alpha=0.5, linewidth=2)
        
        # Draw car
        car = patches.Rectangle(
            (self.car_pos[0] - 1.5, self.car_pos[1] - 0.75), 
            3, 1.5, angle=np.degrees(self.car_angle),
            color='blue', alpha=0.8)
        self.ax.add_patch(car)
        
        # Set plot limits
        self.ax.set_xlim(self.car_pos[0] - 15, self.car_pos[0] + 25)
        self.ax.set_ylim(-self.lane_width * self.lanes - 2, self.lane_width * self.lanes + 4)
        self.ax.set_aspect('equal')
        self.ax.set_title(f"Self-Driving Car Simulation [Speed: {self.speed:.1f} m/s]")
        
        # Add legend
        self.ax.legend([
            plt.Line2D([0], [0], color='b', lw=2, label='Planned Path'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Obstacle'),
            patches.Patch(color='blue', label='Autonomous Vehicle'),
            patches.Patch(color=light_color, label=f'Traffic Light ({self.traffic_light_state})')
        ], ['Planned Path', 'Obstacle', 'Autonomous Vehicle', f'Traffic Light ({self.traffic_light_state})'])
        
        # Stop simulation when car reaches end of road
        if self.car_pos[0] > self.road_length:
            print("Simulation complete: Car reached destination!")
            raise StopIteration

# Run the simulation
simulator = SelfDrivingCarSimulator()
ani = FuncAnimation(simulator.fig, simulator.update, frames=200, interval=50)
plt.show()
            

