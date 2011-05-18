"""Unit tests for the VTK io library"""

# Copyright (C) 2011 Garth N. Wells
#
# This file is part of DOLFIN.
#
# DOLFIN is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DOLFIN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DOLFIN.  If not, see <http://www.gnu.org/licenses/>.
#
# First added:  2011-05-18
# Last changed:

import unittest
from dolfin import *

file_options = ["ascii", "base64", "compressed"]

class VTK_Mesh_Output(unittest.TestCase):

    def test_save_1d_mesh(self):
        mesh = UnitInterval(32)
        File("mesh.pvd") << mesh
        for file_option in file_options:
            File("mesh.pvd", file_option) << mesh

    def test_save_2d_mesh(self):
        mesh = UnitSquare(32, 32)
        File("mesh.pvd") << mesh
        for file_option in file_options:
            File("mesh.pvd", file_option) << mesh

    def test_save_3d_mesh(self):
        mesh = UnitCube(8, 8, 8)
        File("mesh.pvd") << mesh
        for file_option in file_options:
            File("mesh.pvd", file_option) << mesh


class VTK_Point_Function_Output(unittest.TestCase):

    def test_save_1d_scalar(self):
        mesh = UnitInterval(32)
        u = Function(FunctionSpace(mesh, "Lagrange", 2))
        u.vector()[:] = 1.0
        File("u.pvd") << u
        for file_option in file_options:
            File("u.pvd", file_option) << u

    def test_save_2d_scalar(self):
        mesh = UnitSquare(16, 16)
        u = Function(FunctionSpace(mesh, "Lagrange", 2))
        u.vector()[:] = 1.0
        File("u.pvd") << u
        for file_option in file_options:
            File("u.pvd", file_option) << u

    def test_save_3d_scalar(self):
        mesh = UnitCube(8, 8, 8)
        u = Function(FunctionSpace(mesh, "Lagrange", 2))
        u.vector()[:] = 1.0
        File("u.pvd") << u
        for file_option in file_options:
            File("u.pvd", file_option) << u

if __name__ == "__main__":
    unittest.main()
