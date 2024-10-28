from gomokuRL.gomoku_rl.policy import get_policy, Policy
from gomokuRL.gomoku_rl.utils.policy import uniform_policy, _policy_t
from torchrl.data.tensor_specs import (
    DiscreteTensorSpec,
    CompositeSpec,
    UnboundedContinuousTensorSpec,
    BinaryDiscreteTensorSpec,
)
from gomokuRL.gomoku_rl.core import Gomoku
import torch
from tensordict import TensorDict
from omegaconf import DictConfig, OmegaConf
import omegaconf


def _is_action_valid(x: int, y: int, board_size: int):
    return 0 <= x < board_size and 0 <= y < board_size


def make_model(cfg: DictConfig, name='ppo'):
    board_size = cfg.board_size
    device = cfg.device
    action_spec = DiscreteTensorSpec(
        board_size * board_size,
        shape=[
            1,
        ],
        device=device,
    )
    model_cfg = OmegaConf.load('./gomokuRL/cfg/algo/ppo.yaml')
    if (name != 'ppo'):
        model_cfg = OmegaConf.load('./gomokuRL/cfg/algo/dqn.yaml')
    # when using PPO, setting num_envs=1 will cause an error in critic
    observation_spec = CompositeSpec(
        {
            "observation": UnboundedContinuousTensorSpec(
                device=cfg.device,
                shape=[2, 3, board_size, board_size],
            ),
            "action_mask": BinaryDiscreteTensorSpec(
                n=board_size * board_size,
                device=device,
                shape=[2, board_size * board_size],
                dtype=torch.bool,
            ),
        },
        shape=[
            2,
        ],
        device=device,
    )
    model = get_policy(
        name=name,
        cfg=model_cfg,
        action_spec=action_spec,
        observation_spec=observation_spec,
        device=cfg.device,
    )
    return model


class GomokuBoard():
    def __init__(
            self,
            board_size: int = 15,
            model: _policy_t | None = None,
    ):
        self.board_size = board_size
        assert 5 <= self.board_size < 20
        self.model = model or uniform_policy
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self._env = Gomoku(num_envs=1, board_size=board_size, device="cpu")
        self._env.reset()

    def reset(self):
        self._env.reset()

    def done(self):
        return self._env.done.item()

    def _is_action_valid(self, action: int):
        return self._env.is_valid(torch.tensor([action])).item()

    def AI_step(self):

        tensordict = TensorDict(
            {
                "observation": self._env.get_encoded_board(),
                "action_mask": self._env.get_action_mask(),
            },
            batch_size=1,
        )
        with torch.no_grad():
            tensordict = self.model(tensordict).cpu()
        action: int = tensordict["action"].item()
        x = action // self.board_size
        y = action % self.board_size
        assert self._is_action_valid(action)
        self.step([x, y])
        self.board[x][y] = 1
        return y, x

    def step(self, action: list[int]):
        assert 2 == len(action)
        x = action[0]
        y = action[1]

        valid = self._is_action_valid(x * self.board_size + y)

        if not valid:
            return
        self.latest_move = (x, y)
        self._env.step(torch.tensor([x * self.board_size + y]))

    def enemyMove(self, action: list[int]):
        assert 2 == len(action)
        x = action[0]
        y = action[1]
        valid = self._is_action_valid(x * self.board_size + y)

        if not valid:
            return
        self.step([x, y])
        self.board[x][y] = 2


model_name = 'ppo'
model_number = '1'
cfg_path = './gomokuRL/cfg/demo.yaml'
cfg = OmegaConf.load(cfg_path)
# cfg.human_black = False
# print(cfg.human_black)
# print(cfg)
model_path = f'./gomokuRL/pretrained_models/15_15/{model_name}/{model_number}.pt'
model = make_model(cfg, model_name)
model.load_state_dict(torch.load(model_path, map_location=cfg.device))
model.eval()
game = GomokuBoard(
    board_size=cfg.get("board_size", 15),
    model=model,
)


def getAIMove():
    return game.AI_step()


def enemyMove(x, y):
    game.enemyMove([y, x])


def printBoard(board):
    index = [i for i in range(10)] + [0, 1, 2, 3, 4]
    print(" ", end='')
    for i in index: print(i, " ", end="")
    index2 = 0
    print()
    for row in board:
        print(row, index2)
        index2 += 1

# while True:
#     x = int(input("your x move: "))
#     y = int(input("your y move: "))
#     game.enemyMove([y, x])
#     if game.done():
#         print('you win')
#         break
#     game.AI_step()
#     if game.done():
#         print('AI win')
#         break
#     printBoard(game.board)
# printBoard(game.board)
