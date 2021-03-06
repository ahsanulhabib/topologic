# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import unittest
import topologic as tc
import networkx as nx
import numpy as np


class TestPca(unittest.TestCase):
    def test_pca_reduces_to_expected_dimensionality(self):
        graph = nx.barbell_graph(10, 2)

        for edge in graph.edges():
            graph.add_edge(edge[0], edge[1], weight=1)

        expected_dimension = 1

        container = tc.embedding.adjacency_embedding(
            graph,
            maximum_dimensions=5,
            svd_seed=1234
        )

        embedding_reduced = tc.embedding.pca(
            embedding=container.embedding,
            num_components=expected_dimension
        )

        # the embedding reduced by PCA should have the same height as the input embedding
        # but the dimensions should be reduced to exactly the dimension specified in pca call
        self.assertIsNotNone(embedding_reduced)
        self.assertEqual(container.embedding.shape[0], embedding_reduced.shape[0])
        self.assertEqual(embedding_reduced.shape[1], expected_dimension)

    def test_pca_num_components_not_specified_error_raised(self):
        with self.assertRaises(ValueError):
            tc.embedding.pca(np.array([1]), None)

    def test_pca_embedding_not_specified_error_raised(self):
        with self.assertRaises(ValueError):
            tc.embedding.pca(None, 1)
