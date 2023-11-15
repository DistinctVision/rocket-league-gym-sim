from typing import Any, Dict

import rlviser_py as rlviser
import RocketSim as rsim

from rlgym.utils.gamestates import PlayerData, GameState
from rlgym.utils.common_values import BOOST_LOCATIONS


class RLViserRenderer:

    def __init__(self, tick_rate=120/8):
        rlviser.set_boost_pad_locations(BOOST_LOCATIONS)
        self.tick_rate = tick_rate
        self.packet_id = 0

    def render(self, state: GameState, shared_info: Dict[str, Any] = {}) -> Any:
        boost_pad_states = [bool(timer == 0) for timer in state.boost_pads]

        ball = rsim.BallState()
        ball.pos = rsim.Vec(*state.ball.position)
        ball.vel = rsim.Vec(*state.ball.linear_velocity)
        ball.ang_vel = rsim.Vec(*state.ball.angular_velocity)

        car_data = []
        for car in state.players:
            car_state = self._get_car_state(car)
            car_data.append((car.car_id + 1, int(car.team_num), rsim.CarConfig(0), car_state))

        self.packet_id += 1
        rlviser.render(tick_count=self.packet_id, tick_rate=self.tick_rate, game_mode=rsim.GameMode.SOCCAR,
                       boost_pad_states=boost_pad_states, ball=ball, cars=car_data)

    def close(self):
        rlviser.quit()

    # I stole this from RocketSimEngine
    def _get_car_state(self, player: PlayerData):
        car_state = rsim.CarState()
        car_state.pos = rsim.Vec(*player.car_data.position)
        car_state.vel = rsim.Vec(*player.car_data.linear_velocity)
        car_state.ang_vel = rsim.Vec(*player.car_data.angular_velocity)
        car_state.rot_mat = rsim.RotMat(*player.car_data.rotation_mtx().transpose().flatten())

        # car_state.demo_respawn_timer = player.demo_respawn_timer
        car_state.is_on_ground = bool(player.on_ground)
        # car_state.supersonic_time = player.supersonic_time
        car_state.boost = player.boost_amount * 100
        # car_state.time_spent_boosting = player.boost_active_time
        # car_state.handbrake_val = player.handbrake

        car_state.has_jumped = player.has_jump
        # car_state.last_controls.jump = player.is_holding_jump
        # car_state.is_jumping = player.is_jumping
        # car_state.jump_time = player.jump_time

        car_state.has_flipped = player.has_flip
        # car_state.has_double_jumped = player.has_jump
        # car_state.air_time_since_jump = player.air_time_since_jump
        # car_state.flip_time = player.flip_time
        # car_state.last_rel_dodge_torque = rsim.Vec(*player.flip_torque)

        # car_state.is_auto_flipping = player.is_autoflipping
        # car_state.auto_flip_timer = player.autoflip_timer
        # car_state.auto_flip_torque_scale = player.autoflip_direction

        # if player.bump_victim_id is not None:
        #     car_state.car_contact_id = player.bump_victim_id

        return car_state
