from pathlib import Path
from crytic_compile import CryticCompile
from crytic_compile.platform.solc_standard_json import SolcStandardJson
from solc_select import solc_select

from slither import Slither
from slither.slithir.operations import InternalCall, LibraryCall

from tests.utils import _run_all_detectors

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
USING_FOR_TEST_DATA_DIR = Path(TEST_DATA_DIR, "using_for")


def test_using_for_global_collision() -> None:
    solc_select.switch_global_version("0.8.18", always_install=True)
    standard_json = SolcStandardJson()
    for source_file in Path(USING_FOR_TEST_DATA_DIR, "using_for_global_collision").rglob("*.sol"):
        standard_json.add_source_file(Path(source_file).as_posix())
    compilation = CryticCompile(standard_json)
    sl = Slither(compilation)
    _run_all_detectors(sl)


def test_using_for_top_level_same_name() -> None:
    solc_select.switch_global_version("0.8.15", always_install=True)
    slither = Slither(Path(USING_FOR_TEST_DATA_DIR, "using-for-3-0.8.0.sol").as_posix())
    contract_c = slither.get_contract_from_name("C")[0]
    libCall = contract_c.get_function_from_full_name("libCall(uint256)")
    for ir in libCall.all_slithir_operations():
        if isinstance(ir, LibraryCall) and ir.destination == "Lib" and ir.function_name == "a":
            return
    assert False


def test_using_for_top_level_implicit_conversion() -> None:
    solc_select.switch_global_version("0.8.15", always_install=True)
    slither = Slither(Path(USING_FOR_TEST_DATA_DIR, "using-for-4-0.8.0.sol").as_posix())
    contract_c = slither.get_contract_from_name("C")[0]
    libCall = contract_c.get_function_from_full_name("libCall(uint16)")
    for ir in libCall.all_slithir_operations():
        if isinstance(ir, LibraryCall) and ir.destination == "Lib" and ir.function_name == "f":
            return
    assert False


def test_using_for_alias_top_level() -> None:
    solc_select.switch_global_version("0.8.15", always_install=True)
    slither = Slither(
        Path(USING_FOR_TEST_DATA_DIR, "using-for-alias-top-level-0.8.0.sol").as_posix()
    )
    contract_c = slither.get_contract_from_name("C")[0]
    libCall = contract_c.get_function_from_full_name("libCall(uint256)")
    ok = False
    for ir in libCall.all_slithir_operations():
        if isinstance(ir, LibraryCall) and ir.destination == "Lib" and ir.function_name == "b":
            ok = True
    if not ok:
        assert False
    topLevelCall = contract_c.get_function_from_full_name("topLevel(uint256)")
    for ir in topLevelCall.all_slithir_operations():
        if isinstance(ir, InternalCall) and ir.function_name == "a":
            return
    assert False


def test_using_for_alias_contract() -> None:
    solc_select.switch_global_version("0.8.15", always_install=True)
    slither = Slither(
        Path(USING_FOR_TEST_DATA_DIR, "using-for-alias-contract-0.8.0.sol").as_posix()
    )
    contract_c = slither.get_contract_from_name("C")[0]
    libCall = contract_c.get_function_from_full_name("libCall(uint256)")
    ok = False
    for ir in libCall.all_slithir_operations():
        if isinstance(ir, LibraryCall) and ir.destination == "Lib" and ir.function_name == "b":
            ok = True
    if not ok:
        assert False
    topLevelCall = contract_c.get_function_from_full_name("topLevel(uint256)")
    for ir in topLevelCall.all_slithir_operations():
        if isinstance(ir, InternalCall) and ir.function_name == "a":
            return
    assert False


def test_using_for_in_library() -> None:
    solc_select.switch_global_version("0.8.15", always_install=True)
    slither = Slither(Path(USING_FOR_TEST_DATA_DIR, "using-for-in-library-0.8.0.sol").as_posix())
    contract_c = slither.get_contract_from_name("A")[0]
    libCall = contract_c.get_function_from_full_name("a(uint256)")
    for ir in libCall.all_slithir_operations():
        if isinstance(ir, LibraryCall) and ir.destination == "B" and ir.function_name == "b":
            return
    assert False