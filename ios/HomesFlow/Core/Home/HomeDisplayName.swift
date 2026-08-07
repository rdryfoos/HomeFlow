import Foundation

// @covers FR-HOME-04, AC-HOME-15

/// Pure display-name normalization for homes (FR-HOME-04): trims leading and
/// trailing whitespace and collapses every internal run of whitespace
/// (spaces, tabs, newlines) to a single space. No UI, networking, or sync.
enum HomeDisplayName {
    static func normalized(_ raw: String) -> String {
        let separators = CharacterSet.whitespacesAndNewlines
        return raw
            .components(separatedBy: separators)
            .filter { !$0.isEmpty }
            .joined(separator: " ")
    }
}
