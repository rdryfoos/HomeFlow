import XCTest
@testable import HomesFlow

final class HomeDisplayNameTests: XCTestCase {
    func test_AC_HOME_15_normalizes_whitespace() {
        // Leading/trailing whitespace is trimmed.
        XCTAssertEqual(HomeDisplayName.normalized("  Rockport Cottage  "), "Rockport Cottage")

        // Internal runs of spaces collapse to a single space.
        XCTAssertEqual(HomeDisplayName.normalized("Rockport    Cottage"), "Rockport Cottage")

        // Tabs and newlines are treated as whitespace and collapsed.
        XCTAssertEqual(HomeDisplayName.normalized("Rockport\t\tCottage"), "Rockport Cottage")
        XCTAssertEqual(HomeDisplayName.normalized("Rockport\nCottage"), "Rockport Cottage")

        // Mixed whitespace kinds in one run collapse to a single space, with trimming.
        XCTAssertEqual(HomeDisplayName.normalized("\n  Rockport \t\n Cottage \tby the Sea \n"),
                       "Rockport Cottage by the Sea")

        // Already-clean input is returned unchanged.
        XCTAssertEqual(HomeDisplayName.normalized("Rockport Cottage"), "Rockport Cottage")

        // Empty and whitespace-only input normalize to an empty string.
        XCTAssertEqual(HomeDisplayName.normalized(""), "")
        XCTAssertEqual(HomeDisplayName.normalized("   \t\n "), "")
    }
}
