import XCTest
@testable import HomesFlow

// @covers FR-HOME-04, AC-HOME-15

final class HomeDisplayNameNormalizerTests: XCTestCase {

    func test_AC_HOME_15_trims_ends_and_collapses_internal_whitespace() {
        XCTAssertEqual(
            HomeDisplayNameNormalizer.normalize("  Lake   House  "),
            "Lake House"
        )
        XCTAssertEqual(
            HomeDisplayNameNormalizer.normalize("\tCabin\n\nby the\tBay\n"),
            "Cabin by the Bay"
        )
        XCTAssertEqual(HomeDisplayNameNormalizer.normalize("Already Clean"), "Already Clean")
        XCTAssertEqual(HomeDisplayNameNormalizer.normalize("   "), "")
        XCTAssertEqual(HomeDisplayNameNormalizer.normalize(""), "")
    }
}
