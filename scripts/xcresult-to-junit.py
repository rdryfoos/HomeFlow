#!/usr/bin/env python3
"""Convert an .xcresult bundle's test results into a minimal JUnit XML
report, so SpecAssay Gate 2's Rule 6a (proven derives from a passing
proof, not a matching name) can cross-reference XCTest results the
same way it already does for pytest/node:test/vitest's own native
JUnit output. xcodebuild/XCTest have no native JUnit exporter; this
is that adapter, built once, reused by CI and local runs alike.

Usage: xcresult-to-junit.py <path-to.xcresult> <output-path.xml>
"""
import subprocess
import sys
import xml.etree.ElementTree as ET


def leaf_test_cases(node, out):
    if node.get("nodeType") == "Test Case":
        out.append(node)
        return
    for child in node.get("children", []):
        leaf_test_cases(child, out)


def main():
    if len(sys.argv) != 3:
        print("usage: xcresult-to-junit.py <path.xcresult> <output.xml>", file=sys.stderr)
        return 2
    xcresult_path, out_path = sys.argv[1], sys.argv[2]

    proc = subprocess.run(
        ["xcrun", "xcresulttool", "get", "test-results", "tests",
         "--path", xcresult_path, "--compact"],
        capture_output=True, text=True, check=True,
    )
    import json
    data = json.loads(proc.stdout)

    cases = []
    for top in data.get("testNodes", []):
        leaf_test_cases(top, cases)

    testsuite = ET.Element("testsuite", name="HomesFlowTests", tests=str(len(cases)))
    failures = 0
    for case in cases:
        # nodeIdentifier is "ClassName/test_method_name()"; JUnit wants
        # classname + name split the same way pytest's own does.
        identifier = case.get("nodeIdentifier", case.get("name", "unknown"))
        classname, _, name = identifier.rpartition("/")
        name = name.rstrip("()")
        testcase = ET.SubElement(
            testsuite, "testcase",
            classname=classname or "HomesFlowTests",
            name=name,
            time=str(case.get("durationInSeconds", 0)),
        )
        if case.get("result") != "Passed":
            failures += 1
            ET.SubElement(testcase, "failure", message=f"XCTest result: {case.get('result')}")

    testsuite.set("failures", str(failures))
    testsuites = ET.Element("testsuites")
    testsuites.append(testsuite)
    ET.ElementTree(testsuites).write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"wrote {out_path}: {len(cases)} testcases, {failures} failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
