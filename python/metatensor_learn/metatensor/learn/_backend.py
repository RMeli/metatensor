# This file defines the default set of classes to use in metatensor-learn
#
# The code from metatensor-learn can be used in two different modes: either pure Python
# mode or TorchScript mode. In the second case, we need to use a different version of
# the classes above; to do so without having to rewrite everything, we re-import
# metatensor-learn in a special context.
#
# See metatensor-torch/metatensor/torch/learn.py for more information.
#
# Any change to this file MUST be also be made to `metatensor/torch/learn.py`.

import re
import warnings

import metatensor


try:
    import torch

    _HAS_TORCH = True
except ImportError:
    _HAS_TORCH = False


Labels = metatensor.Labels
LabelsEntry = metatensor.LabelsEntry
TensorBlock = metatensor.TensorBlock
TensorMap = metatensor.TensorMap


def torch_jit_is_scripting():
    return False


_VERSION_REGEX = re.compile(r"(\d+)\.(\d+)\.*.")


def _version_at_least(version, expected):
    version = tuple(map(int, _VERSION_REGEX.match(version).groups()))
    expected = tuple(map(int, _VERSION_REGEX.match(expected).groups()))

    return version >= expected


# Warning: this function (as all functions in this module) is part of the public API of
# metatensor-learn, updating it means that new versions of metatensor-torch will not be
# able to work with old versions of metatensor-learn, so any update should be treated as
# a breaking change.
def isinstance_metatensor(value, typename):
    assert typename in ("Labels", "TensorBlock", "TensorMap")

    if _HAS_TORCH and isinstance(value, torch.ScriptObject):
        is_metatensor_torch_class = "metatensor" in str(value._type())
        if is_metatensor_torch_class:
            warnings.warn(
                "Trying to use code from ``metatensor.learn`` with objects from "
                "metatensor-torch, you should use the code from "
                "`metatensor.torch.learn` instead",
                stacklevel=2,
            )

    if typename == "Labels":
        return isinstance(value, Labels)
    elif typename == "TensorBlock":
        return isinstance(value, TensorBlock)
    elif typename == "TensorMap":
        return isinstance(value, TensorMap)
    else:
        return False
