"""
Zhifeng's Blender Utilities
Copyright (C) 2024  Zhifeng Wang 王之枫

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License only.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import numpy as np

from fun.disjoint_set import DisjointSet
from consts import POSITION_KEY_STRING, FACE_INDEX_KEY_STRING

MAZE_ROW_LEN = 5
MAZE_COL_LEN = 5
MAZE_TOTAL_LEN = MAZE_ROW_LEN * MAZE_COL_LEN

BLOCK_RADIUS = 1
BLOCK_LENGTH = 2 * BLOCK_RADIUS
ISLAND_RADIUS = 0.2
BRIDGE_LENGTH = BLOCK_RADIUS - ISLAND_RADIUS

FIRST_BLOCK_ROW_POS = -(MAZE_ROW_LEN * BLOCK_RADIUS)
FIRST_BLOCK_COL_POS = -(MAZE_COL_LEN * BLOCK_RADIUS)

CORD_ELEM_LEN = 3
ISLAND_CORD_LEN = 4
ISLAND_ELEM_LEN = CORD_ELEM_LEN * ISLAND_CORD_LEN


def calc_graph_node_i(row_i, col_i):
    return row_i * MAZE_COL_LEN + col_i


def calc_block_center(row_i, col_i):
    return (
        FIRST_BLOCK_ROW_POS + row_i * BLOCK_LENGTH + BLOCK_RADIUS,
        FIRST_BLOCK_COL_POS + col_i * BLOCK_LENGTH + BLOCK_RADIUS,
    )


def make_edge_list():
    ans_edge_list = []
    for row_i in range(1, MAZE_ROW_LEN):
        ans_edge_list.append(
            (calc_graph_node_i(row_i - 1, 0), calc_graph_node_i(row_i, 0))
        )

    for col_i in range(1, MAZE_COL_LEN):
        ans_edge_list.append(
            (calc_graph_node_i(0, col_i - 1), calc_graph_node_i(0, col_i))
        )

    for row_i in range(1, MAZE_ROW_LEN):
        for col_i in range(1, MAZE_COL_LEN):
            ans_edge_list.append(
                (calc_graph_node_i(row_i - 1, col_i), calc_graph_node_i(row_i, col_i))
            )
            ans_edge_list.append(
                (calc_graph_node_i(row_i, col_i - 1), calc_graph_node_i(row_i, col_i))
            )
    return ans_edge_list


def make_maze_edge_list(edge_list):
    uf = DisjointSet(MAZE_TOTAL_LEN)
    ans_edge_list = []
    for node_0_i, node_1_i in edge_list:
        if uf.union(node_0_i, node_1_i) == True:
            ans_edge_list.append((node_0_i, node_1_i))
    return ans_edge_list


def push_vertice_positions_to_vertice_and_face_list(
    vertice_list_mut_ref, face_idx_list_mut_ref, row_i, col_i
):
    block_center_x, block_center_y = calc_block_center(row_i, col_i)
    prev_v_len = int(len(vertice_list_mut_ref) / CORD_ELEM_LEN)
    vertice_list_mut_ref.extend(
        (
            block_center_x - ISLAND_RADIUS,
            block_center_y - ISLAND_RADIUS,
            0,
            block_center_x - ISLAND_RADIUS,
            block_center_y + ISLAND_RADIUS,
            0,
            block_center_x + ISLAND_RADIUS,
            block_center_y - ISLAND_RADIUS,
            0,
            block_center_x + ISLAND_RADIUS,
            block_center_y + ISLAND_RADIUS,
            0,
        )
    )

    face_idx_list_mut_ref.extend(
        (
            prev_v_len,
            prev_v_len + 1,
            prev_v_len + 2,
            prev_v_len + 2,
            prev_v_len + 1,
            prev_v_len + 3,
        )
    )


def make_islands_geometry():
    vertice_list = []
    face_idx_list = []
    for row_i in range(0, MAZE_ROW_LEN):
        for col_i in range(0, MAZE_COL_LEN):
            push_vertice_positions_to_vertice_and_face_list(
                vertice_list, face_idx_list, row_i, col_i
            )
    return (vertice_list, face_idx_list)


def link_islands(maze_edge_list, face_idx_list_mut_ref):
    for island_0_i, island_1_i in maze_edge_list:
        island_0_cord_begin_i = island_0_i * ISLAND_CORD_LEN
        island_1_cord_begin_i = island_1_i * ISLAND_CORD_LEN
        if island_0_i + 1 == island_1_i:
            top_left_cord_i = island_0_cord_begin_i + 1
            top_right_cord_i = island_1_cord_begin_i + 0
            bot_left_cord_i = island_0_cord_begin_i + 3
            bot_right_cord_i = island_1_cord_begin_i + 2
            face_idx_list_mut_ref.extend(
                (
                    top_left_cord_i,
                    top_right_cord_i,
                    bot_left_cord_i,
                    bot_left_cord_i,
                    top_right_cord_i,
                    bot_right_cord_i,
                )
            )
        else:
            top_left_cord_i = island_0_cord_begin_i + 2
            top_right_cord_i = island_0_cord_begin_i + 3
            bot_left_cord_i = island_1_cord_begin_i + 0
            bot_right_cord_i = island_1_cord_begin_i + 1
            face_idx_list_mut_ref.extend(
                (
                    top_left_cord_i,
                    top_right_cord_i,
                    bot_left_cord_i,
                    bot_left_cord_i,
                    top_right_cord_i,
                    bot_right_cord_i,
                )
            )


import json


def main():
    edge_list = make_edge_list()
    np.random.shuffle(edge_list)
    maze_edge_list = make_maze_edge_list(edge_list)
    vertice_list, face_idx_list = make_islands_geometry()
    link_islands(maze_edge_list, face_idx_list)

    with open(input("Input output file path: "), "w") as out_file:
        json.dump(
            {FACE_INDEX_KEY_STRING: face_idx_list, POSITION_KEY_STRING: vertice_list},
            out_file,
        )


main()
