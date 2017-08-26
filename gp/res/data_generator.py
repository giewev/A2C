import numpy as np


class GenerateData:
    def __init__(self, config):
        """
        it just take the config file which contain all paths the generator needs
        :param config: configuration
        """
        np.random.seed(2)
        x = np.load(config.x_path)
        self.rewards = np.load(config.rewards_path)

        np.random.shuffle(x)
        self.y = x[:, 1:]
        self.x = x[:, :-1]

        np.random.shuffle(self.rewards)
        self.actions = None
        self.config = config

        self.prepare_actions()

        self.rewards = np.expand_dims(self.rewards, axis=2)

        self.xtest = self.x[self.config.num_episodes_train:config.num_episodes_train + config.num_episodes_test]
        self.x = self.x[:self.config.num_episodes_train]
        self.ytest = self.y[self.config.num_episodes_train:config.num_episodes_train + config.num_episodes_test]
        self.y = self.y[:self.config.num_episodes_train]
        self.actionstest = self.actions[
                           self.config.num_episodes_train:config.num_episodes_train + config.num_episodes_test]
        self.actions = self.actions[:self.config.num_episodes_train]
        self.rewardstest = self.rewards[
                           self.config.num_episodes_train:config.num_episodes_train + config.num_episodes_test]
        self.rewards = self.rewards[:self.config.num_episodes_train]

    def next_batch(self):
        """
        :return: a tuple of all batches

        """
        while True:
            idx = np.random.choice(self.config.num_episodes_train, self.config.batch_size)
            self.current_x = self.x[idx]
            self.current_y = self.y[idx]
            self.current_actions = self.actions[idx]
            self.current_rewards = self.rewards[idx]
            for i in range(0, self.config.all_seq_length, self.config.truncated_time_steps):
                if i == 0:
                    new_sequence = True
                else:
                    new_sequence = False
                batch_x = self.current_x[:, i:i + self.config.truncated_time_steps, :]
                batch_y = self.current_y[:, i:i + self.config.truncated_time_steps, :]
                batch_actions = self.current_actions[:, i:i + self.config.truncated_time_steps, :]
                batch_rewards = self.current_rewards[:, i:i + self.config.truncated_time_steps, :]
                yield batch_x, batch_y, batch_actions, batch_rewards, new_sequence

    def prepare_actions(self):
        self.actions = np.zeros(
            (self.config.num_episodes, self.config.all_seq_length, self.config.action_dim))
        actions = np.int32(np.load(self.config.actions_path))
        np.random.shuffle(actions)
        self.actions[:, actions[:self.config.num_episodes]] = 1
