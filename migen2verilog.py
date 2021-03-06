from migen.fhdl.verilog import convert
from migen.build.xilinx import common, vivado
from sys import argv
from os import chdir, getcwd
from os.path import basename, dirname


def snake_to_camel_case(snake):
    words = snake.split('_')
    return "".join((w.capitalize() for w in words))


if __name__ == "__main__":
    if len(argv) != 3:
        print("usage: %s migen_file.py out_verilog.v" % argv[0])

    filename = argv[1]
    module_name = basename(filename).replace(".py", "")
    class_name = snake_to_camel_case(module_name)

    call_dir = getcwd()
    chdir(dirname(filename))
    module = getattr(__import__("cores.%s" % module_name), module_name)
    core = getattr(module, class_name)

    chdir(call_dir)
    device = core()

    so = dict(common.xilinx_special_overrides)
    so.update(common.xilinx_s7_special_overrides)
    
    convert(device, ios=device.ios, name=module_name, special_overrides=so, attr_translate=vivado.XilinxVivadoToolchain.attr_translate).write(argv[2])
