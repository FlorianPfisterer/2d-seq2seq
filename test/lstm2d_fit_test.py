from unittest import TestCase
import torch
from model.lstm2d import LSTM2d

class LSTM2dFitTest(TestCase):
    """
    Unit tests for the 2D-LSTM in inference mode.
    """
    embed_dim = 2
    encoder_state_dim = 5
    cell_state_dim = 3

    max_input_len = 3
    max_output_len = max_input_len

    vocab_size = 3

    def setUp(self):
        torch.manual_seed(42)
        self.lstm = LSTM2d(embed_dim=self.embed_dim, state_dim_2d=self.cell_state_dim,
                           encoder_state_dim=self.encoder_state_dim, max_input_len=self.max_input_len,
                           max_output_len=self.max_output_len, vocab_size=self.vocab_size)

    def test_fits_small_dataset(self):
        """
        Tests if the model can fit a simple, small, random dataset (i.e. validate that it actually learns something).
        """
        dataset_size = 4
        x = torch.randint(0, self.vocab_size, (self.max_input_len, dataset_size), dtype=torch.long)
        y = x.clone()   # should learn the identity function
        y_t = y.t()

        loss = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.lstm.parameters(), lr=0.1)

        self.lstm.train()

        initial_loss = -1
        last_loss = -1
        for _ in range(200):
            y_pred = self.lstm.forward(x, y).permute(1, 0, 2)
            loss_value = loss(y_pred, y_t)

            last_loss = loss_value.item()
            if initial_loss < 0:
                initial_loss = last_loss

            optimizer.zero_grad()
            loss_value.backward()
            optimizer.step()

        print("from {} to {}".format(initial_loss, last_loss))
        self.assertTrue(last_loss < initial_loss, 'The model did not learn anything.')
