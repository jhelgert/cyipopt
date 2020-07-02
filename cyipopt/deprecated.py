# -*- coding: utf-8 -*-

"""Module with utilities to aid deprecation within CyIpopt."""


from functools import wraps
import warnings

from ipopt_wrapper import Problem


__all__ = ["problem"]


def deprecated_warning(new_name):
	"""Decorator that issues a FutureWarning for deprecated functionality.

	Parameters
	----------
		new_name : :obj:`str`
			The name of the object replacing the deprecated one.

	Returns
	-------
		:obj:`decorator`
	"""

	def decorate(func):
		
		@wraps(func)
		def wrapper(*args, **kwargs):
			if hasattr(func, "__objclass__"):
				what = "method"
				class_name = getattr(func, "__objclass__").__name__
				msg = generate_deprecation_warning_msg(what, old_name, new_name,
					class_name=class_name)
			else:
				what = "function"
				msg = generate_deprecation_warning_msg(what, old_name, new_name)
			warnings.warn(msg, FutureWarning)
			return func(*args, **kwargs)

		old_name = getattr(func, "__name__")
		return wrapper

	return decorate


class problem:
	"""Class to continue support for old API.

	.. deprecated:: 1.0.0
          :class:`problem` will be removed in CyIpopt 1.1.0, it is replaced 
          by :class:`Problem` because the latter complies with PEP8.

	For full documentation of this class including its attributes and methods 
	please see :class:`Problem`.

	This class acts as a wrapper to the new :class:`Problem` class. It simply 
	issues a :warning:`FutureWarning` to the user before passing all args and 
	kwargs through to :class:`Problem`.

	Returns
	-------
		:obj:`Problem`
			Instance created with the `args` and `kwargs` parameters.

	"""

	def __new__(self, *args, **kwargs):
		msg = generate_deprecation_warning_msg("class", "problem", "Problem")
		warnings.warn(msg, FutureWarning)
		return Problem(*args, **kwargs)


def generate_deprecation_warning_msg(what, old_name, new_name, class_name=None):
	"""Helper function to create user-friendly deprecation messages.

	Parameters
	----------
	what : str
		The type of object that is being deprecated. Expected values are 
		:str:`class`, :str:`function` and :str:`method`.
	old_name : str
		The name of the object being deprecated.
	new_name : str
		The name of the object replacing the deprecated object.
	class_name : str, optional
		The class name if the object being deprecated is a :obj:`class`. 
		Default value is :obj:`None`.

	Returns
	-------
		str
			The nicely formatted informative :obj:`str` to be outputted as the 
			warning message.

	Raises
	------
		ValueError
			If a :arg:`class_name` is supplied but :arg:`what` does not equal 
			:str:`"class"`.
	"""
	if what == "class" and class_name is not None:
		msg = "Incorrect use of function arguments."
		raise ValueError(msg)
	if class_name is not None:
		class_name_msg = f"in class '{str(class_name)}' "
	else:
		class_name_msg = ""
	msg = (f"The {what} named '{old_name}' {class_name_msg}will soon be "
		f"deprecated in CyIpopt. Please replace all uses and use '{new_name}' "
		"going forward.")
	return msg