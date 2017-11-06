import pytest

from liblfort.semantic.analyze import (create_symbol_table, Integer, Real,
        UndeclaredVariableError, VariableVisitor)
from liblfort.ast import parse

def test_variables():
    source = """\
module test
implicit none
contains

    subroutine sub1(a, b)
    integer, intent(in) :: a
    real, intent(out) :: b
    b = a + 1
    end subroutine

end module
"""
    tree = parse(source)
    symbol_table = create_symbol_table(tree)
    assert "a" in symbol_table
    assert isinstance(symbol_table["a"], Integer)
    assert symbol_table["a"].varname == "a"
    assert "b" in symbol_table
    assert isinstance(symbol_table["b"], Real)
    assert symbol_table["b"].varname == "b"
    assert not "c" in symbol_table

def test_unknown_type1():
    source = """\
module test
implicit none
contains

    subroutine sub1(a)
    integer, intent(in) :: a
    a = b
    end subroutine

end module
"""
    tree = parse(source)
    symbol_table = create_symbol_table(tree)
    v = VariableVisitor(symbol_table)
    with pytest.raises(UndeclaredVariableError):
        v.visit(tree)

def test_unknown_type2():
    source = """\
module test
implicit none
contains

    subroutine sub1(a)
    integer, intent(in) :: a
    a = (1+b)**2
    end subroutine

end module
"""
    tree = parse(source)
    symbol_table = create_symbol_table(tree)
    v = VariableVisitor(symbol_table)
    with pytest.raises(UndeclaredVariableError):
        v.visit(tree)

def test_unknown_type3():
    source = """\
module test
implicit none
contains

    subroutine sub1(a)
    integer, intent(in) :: a
    a = (1+a)**2
    end subroutine

end module
"""
    tree = parse(source)
    symbol_table = create_symbol_table(tree)
    v = VariableVisitor(symbol_table)
    v.visit(tree)
