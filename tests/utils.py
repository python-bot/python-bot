from python_bot.common.utils.packer import pack_string, unpack_string


def test_pack_unpack():
    assert len(pack_string(10 ** 100 + 1)) == 53
    data = [133124513, "Hello world"]
    assert (unpack_string(pack_string(*data), types=[int, str])) == data
    assert pack_string("demo") == "WMyq{"
