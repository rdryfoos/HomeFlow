import Foundation

// @covers FR-HOME-04, AC-HOME-15

/// Pure helper: canonicalize home display names.
/// Trims ends and collapses internal whitespace runs to a single space.
/// No UI; no sync (`FR-HOME-04`).
enum HomeDisplayNameNormalizer {

    static func normalize(_ name: String) -> String {
        let trimmed = name.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return "" }

        return trimmed
            .split(whereSeparator: { $0.isWhitespace })
            .joined(separator: " ")
    }
}
