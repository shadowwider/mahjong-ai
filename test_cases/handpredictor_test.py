from MLUtils import HandPredictor
import numpy as np
import random
import unittest
def test(args):
	suite = unittest.defaultTestLoader.loadTestsFromTestCase(Hand_predictor_test)
	unittest.TextTestRunner().run(suite)

class Hand_predictor_test(unittest.TestCase):
	def test_dimension(self):
		model = HandPredictor(learning_rate = 1e-2)
		in_matrix = np.random.rand(3, 4, 9, 4)
		out_matrix, _ = model.predict(in_matrix)
		self.assertEqual(out_matrix.shape, (3, 34))