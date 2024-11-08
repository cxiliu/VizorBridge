from abc import abstractmethod
import time
import threading
import roslibpy

# class temaplate for robot interface 
# ABB and KUKA classes inherit from it

class RobotInterface():
    def __init__(self, name, client):
        self.name = name
        self.pause = False
        self.stop = False
        self.client = client
        
        exec_listener = roslibpy.Topic(self.client, f'/{self.name}/execute', 'trajectory_msgs/JointTrajectory')
        exec_listener.subscribe(self.execute_trajectory)
        
        command_listener = roslibpy.Topic(self.client, f'/Robot/control', 'std_msgs/String')
        command_listener.subscribe(self.process_command)

        print(f"{self.name} Connected: {self.client.is_connected}")

    @abstractmethod
    def get_current_state(self):
        pass

    @abstractmethod
    def go_to_home(self):
        pass
    
    @abstractmethod
    def execute(self, frames):
        pass

    @abstractmethod
    def cleanup(self):
        pass
    
    def execute_trajectory(self, msg):
        frames = msg['points']
        print (f"execution command received - length: {len(frames)}")
        thread = threading.Thread(target=self.execute, args=(frames,))
        thread.start()
        print (f"execution thread started")

    def process_command(self, msg):
        print(f"{self.name} command: {msg['data']}")

        if msg['data'] == "start":
            self.go_to_home()
        elif msg['data'] == "pause":
            self.pause = True # pause the execution loop
        elif msg['data'] == "resume":
            self.pause = False # resume the execution loop
        elif msg['data'] == "stop":
            self.stop = True # exit the execution loop
        elif msg['data'] == "home":
            self.go_to_home()

    def init_home(self, auto_home):
        self.get_current_state()
        if auto_home:
            time.sleep(2)
            self.go_to_home()
    
    def cleanup_connections(self):
        self.client.terminate()
        self.client.close()