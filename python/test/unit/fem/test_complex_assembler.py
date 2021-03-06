# Copyright (C) 2018 Igor A. Baratta
#
# This file is part of DOLFIN (https://www.fenicsproject.org)
#
# SPDX-License-Identifier:    LGPL-3.0-or-later
"""Unit tests for assembly in complex mode"""

import numpy as np
import pytest

import dolfin
import ufl
from ufl import dx, grad, inner

pytestmark = pytest.mark.skipif(
    not dolfin.has_petsc_complex(), reason="Only works in complex mode.")


def test_complex_assembly():
    """Test assembly of complex matrices and vectors"""

    mesh = dolfin.generation.UnitSquareMesh(dolfin.MPI.comm_world, 10, 10)
    P2 = ufl.FiniteElement("Lagrange", mesh.ufl_cell(), 2)
    V = dolfin.function.functionspace.FunctionSpace(mesh, P2)

    u = dolfin.function.argument.TrialFunction(V)
    v = dolfin.function.argument.TestFunction(V)

    g = dolfin.function.constant.Constant(-2 + 3.0j)
    j = dolfin.function.constant.Constant(1.0j)

    a_real = inner(u, v) * dx
    L1 = inner(g, v) * dx

    bnorm = dolfin.fem.assemble(L1).norm(dolfin.cpp.la.Norm.l1)
    b_norm_ref = abs(-2 + 3.0j)
    assert np.isclose(bnorm, b_norm_ref)
    A0_norm = dolfin.fem.assemble(a_real).norm(dolfin.cpp.la.Norm.frobenius)

    a_imag = j * inner(u, v) * dx
    f = dolfin.Expression("j*sin(2*pi*x[0])", degree=2)
    L0 = inner(f, v) * dx
    A1_norm = dolfin.fem.assemble(a_imag).norm(dolfin.cpp.la.Norm.frobenius)
    assert np.isclose(A0_norm, A1_norm)
    b1_norm = dolfin.fem.assemble(L0).norm(dolfin.cpp.la.Norm.l2)

    a_complex = (1 + j) * inner(u, v) * dx
    f = dolfin.Expression("sin(2*pi*x[0])", degree=2)
    L2 = inner(f, v) * dx
    A2_norm = dolfin.fem.assemble(a_complex).norm(dolfin.cpp.la.Norm.frobenius)
    assert np.isclose(A1_norm, A2_norm / np.sqrt(2))
    b2_norm = dolfin.fem.assemble(L2).norm(dolfin.cpp.la.Norm.l2)
    assert np.isclose(b2_norm, b1_norm)


def test_complex_assembly_solve():
    """Solve a positive definite helmholtz problem and verify solution
    with the method of manufactured solutions

    """

    degree = 3
    mesh = dolfin.generation.UnitSquareMesh(dolfin.MPI.comm_world, 20, 20)
    P = ufl.FiniteElement("Lagrange", mesh.ufl_cell(), degree)
    V = dolfin.function.functionspace.FunctionSpace(mesh, P)

    # Define source term
    A = 1 + 2 * (2 * np.pi)**2
    f = dolfin.Expression(
        "(1.+j)*A*cos(2*pi*x[0])*cos(2*pi*x[1])", degree=degree, A=A)

    # Variational problem
    u = dolfin.function.argument.TrialFunction(V)
    v = dolfin.function.argument.TestFunction(V)
    C = dolfin.function.constant.Constant(1 + 1j)
    a = C * inner(grad(u), grad(v)) * dx + C * inner(u, v) * dx
    L = inner(f, v) * dx

    # Assemble
    A = dolfin.fem.assemble(a)
    b = dolfin.fem.assemble(L)

    # Create solver
    solver = dolfin.cpp.la.PETScKrylovSolver(mesh.mpi_comm())
    dolfin.cpp.la.PETScOptions.set("ksp_type", "preonly")
    dolfin.cpp.la.PETScOptions.set("pc_type", "lu")
    solver.set_from_options()
    x = dolfin.cpp.la.PETScVector()
    solver.set_operator(A)
    solver.solve(x, b)

    # Reference Solution
    ex = dolfin.Expression("cos(2*pi*x[0])*cos(2*pi*x[1])", degree=degree)
    u_ref = dolfin.interpolate(ex, V)

    xnorm = x.norm(dolfin.cpp.la.Norm.l2)
    x_ref_norm = u_ref.vector().norm(dolfin.cpp.la.Norm.l2)
    assert np.isclose(xnorm, x_ref_norm)
