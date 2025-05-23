import io
import os

import pytest
import torch

import metatensor.torch as mts


def test_detach():
    # this only runs basic checks functionality checks, and that the code produces
    # output with the right type
    tensor = mts.load(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "metatensor_operations",
            "tests",
            "data",
            "qm7-power-spectrum.mts",
        )
    )
    tensor = mts.requires_grad(tensor)

    assert isinstance(tensor, torch.ScriptObject)
    assert tensor._type().name() == "TensorMap"

    for block in tensor:
        assert block.values.requires_grad

    tensor = mts.detach(tensor)

    assert isinstance(tensor, torch.ScriptObject)
    assert tensor._type().name() == "TensorMap"

    for block in tensor:
        assert not block.values.requires_grad


@pytest.mark.skipif(os.environ.get("PYTORCH_JIT") == "0", reason="requires TorchScript")
def test_save_load():
    with io.BytesIO() as buffer:
        torch.jit.save(mts.detach, buffer)
        buffer.seek(0)
        torch.jit.load(buffer)
