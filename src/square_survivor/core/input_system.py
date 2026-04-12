import pygame
from enum import Enum, auto
from typing import Dict, Set, List, Optional

class InputAction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    CONFIRM = auto()
    DASH = auto()
    BACK = auto()
    QUIT = auto()
    PAUSE = auto()
    TOGGLE_FULLSCREEN = auto()

class InputSystem:
    def __init__(self):
        # Physical mappings
        self.key_map: Dict[int, InputAction] = {
            pygame.K_w: InputAction.UP,
            pygame.K_UP: InputAction.UP,
            pygame.K_s: InputAction.DOWN,
            pygame.K_DOWN: InputAction.DOWN,
            pygame.K_a: InputAction.LEFT,
            pygame.K_LEFT: InputAction.LEFT,
            pygame.K_d: InputAction.RIGHT,
            pygame.K_RIGHT: InputAction.RIGHT,
            pygame.K_SPACE: InputAction.CONFIRM,
            pygame.K_RETURN: InputAction.CONFIRM,
            pygame.K_ESCAPE: InputAction.PAUSE,
            pygame.K_F11: InputAction.TOGGLE_FULLSCREEN,
        }
        
        # Playstation 4 Controller Mappings (User verified)
        # Button 0 is X (Cross)
        self.joy_button_map: Dict[int, InputAction] = {
            0: InputAction.CONFIRM,
            1: InputAction.PAUSE,
        }
        
        # State tracking
        self.pressed_actions: Set[InputAction] = set()
        self.just_pressed_actions: Set[InputAction] = set()
        self.joysticks: List[pygame.joystick.Joystick] = []
        
        # Analog stick discrete state (for menu flicking)
        # Dictionary of {joy_id: {axis_index: last_value}}
        self.last_axis_states: Dict[int, Dict[int, float]] = {}
        
        self._init_joysticks()

    def _init_joysticks(self):
        pygame.joystick.init()
        for i in range(pygame.joystick.get_count()):
            joy = pygame.joystick.Joystick(i)
            joy.init()
            self.joysticks.append(joy)

    def update(self, events: List[pygame.event.Event]):
        """Update the input state based on the events from this frame."""
        self.just_pressed_actions.clear()
        
        # Discrete Analog Stick Handling (Flick detection)
        threshold = 0.5
        for joy_idx, joy in enumerate(self.joysticks):
            if joy_idx not in self.last_axis_states:
                self.last_axis_states[joy_idx] = {}
            
            for axis in range(min(joy.get_numaxes(), 4)): # Check first 4 axes
                try:
                    val = joy.get_axis(axis)
                    last_val = self.last_axis_states[joy_idx].get(axis, 0.0)
                    
                    # Detect positive flick
                    if val > threshold and last_val <= threshold:
                        if axis == 0: self._trigger_action(InputAction.RIGHT, True)
                        elif axis == 1: self._trigger_action(InputAction.DOWN, True)
                    # Detect negative flick
                    elif val < -threshold and last_val >= -threshold:
                        if axis == 0: self._trigger_action(InputAction.LEFT, True)
                        elif axis == 1: self._trigger_action(InputAction.UP, True)
                    
                    # Release state when returning toward center
                    if abs(val) < threshold * 0.8 and abs(last_val) >= threshold * 0.8:
                        if axis == 0:
                            self._trigger_action(InputAction.LEFT, False)
                            self._trigger_action(InputAction.RIGHT, False)
                        elif axis == 1:
                            self._trigger_action(InputAction.UP, False)
                            self._trigger_action(InputAction.DOWN, False)
                            
                    self.last_axis_states[joy_idx][axis] = val
                except:
                    pass

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_map:
                    action = self.key_map[event.key]
                    self.pressed_actions.add(action)
                    self.just_pressed_actions.add(action)
                
                # Special case: Alt+Enter for Fullscreen
                if event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):
                    self.pressed_actions.add(InputAction.TOGGLE_FULLSCREEN)
                    self.just_pressed_actions.add(InputAction.TOGGLE_FULLSCREEN)
                    
            elif event.type == pygame.KEYUP:
                if event.key in self.key_map:
                    action = self.key_map[event.key]
                    if action in self.pressed_actions:
                        self.pressed_actions.remove(action)
                        
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in self.joy_button_map:
                    action = self.joy_button_map[event.button]
                    self.pressed_actions.add(action)
                    self.just_pressed_actions.add(action)
                    
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in self.joy_button_map:
                    action = self.joy_button_map[event.button]
                    if action in self.pressed_actions:
                        self.pressed_actions.remove(action)

            # Optional: D-Pad support (mapped to Axis or Hat depending on controller)
            elif event.type == pygame.JOYHATMOTION:
                # Hat index 0 (standard D-pad)
                x, y = event.value
                # Handle Y (Up/Down)
                if y == 1: 
                    self._trigger_action(InputAction.UP, True)
                    self._trigger_action(InputAction.DOWN, False)
                elif y == -1: 
                    self._trigger_action(InputAction.DOWN, True)
                    self._trigger_action(InputAction.UP, False)
                else:
                    self._trigger_action(InputAction.UP, False)
                    self._trigger_action(InputAction.DOWN, False)
                
                # Handle X (Left/Right)
                if x == -1:
                    self._trigger_action(InputAction.LEFT, True)
                    self._trigger_action(InputAction.RIGHT, False)
                elif x == 1:
                    self._trigger_action(InputAction.RIGHT, True)
                    self._trigger_action(InputAction.LEFT, False)
                else:
                    self._trigger_action(InputAction.LEFT, False)
                    self._trigger_action(InputAction.RIGHT, False)

    def _trigger_action(self, action: InputAction, is_down: bool):
        if is_down:
            if action not in self.pressed_actions:
                self.pressed_actions.add(action)
                self.just_pressed_actions.add(action)
        else:
            if action in self.pressed_actions:
                self.pressed_actions.remove(action)

    def is_pressed(self, action: InputAction) -> bool:
        """Check if an action is currently being held down."""
        # Special case: DASH is a synonym for CONFIRM in gameplay
        if action == InputAction.DASH:
            return InputAction.CONFIRM in self.pressed_actions
        return action in self.pressed_actions

    def was_just_pressed(self, action: InputAction) -> bool:
        """Check if an action was triggered this frame."""
        if action == InputAction.DASH:
            return InputAction.CONFIRM in self.just_pressed_actions
        return action in self.just_pressed_actions

    def consume_action(self, action: InputAction):
        """Consume a 'just pressed' action so other systems don't see it this frame."""
        if action in self.just_pressed_actions:
            self.just_pressed_actions.remove(action)
        if action == InputAction.CONFIRM and InputAction.DASH in self.just_pressed_actions:
            self.just_pressed_actions.remove(InputAction.DASH)

    def clear_all(self):
        """Reset all input states (used during state transitions)."""
        self.pressed_actions.clear()
        self.just_pressed_actions.clear()

    def get_movement_vector(self) -> pygame.Vector2:
        """Returns a normalized Vector2 based on current movement actions."""
        # For movement, we should also check analog sticks if present
        dx, dy = 0.0, 0.0
        
        if self.is_pressed(InputAction.UP): dy -= 1
        if self.is_pressed(InputAction.DOWN): dy += 1
        if self.is_pressed(InputAction.LEFT): dx -= 1
        if self.is_pressed(InputAction.RIGHT): dx += 1
        
        # Check Analog Stick (Axis 0 and 1 are usually Left Stick)
        for joy in self.joysticks:
            try:
                ax = joy.get_axis(0)
                ay = joy.get_axis(1)
                # Deadzone
                if abs(ax) > 0.2: dx += ax
                if abs(ay) > 0.2: dy += ay
            except:
                pass
                
        vec = pygame.Vector2(dx, dy)
        if vec.length() > 1:
            vec.normalize_ip()
        return vec
