import Foundation
import Vision

struct OCRResult: Codable {
    let imagePath: String
    let text: String
}

func recognize(path: String) throws -> String {
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    let preferredLanguages = ["zh-Hans", "zh-Hans-US", "en-US"]
    let supportedLanguages = (try? request.supportedRecognitionLanguages()) ?? []
    let enabledLanguages = preferredLanguages.filter { supportedLanguages.contains($0) }
    if !enabledLanguages.isEmpty {
        request.recognitionLanguages = enabledLanguages
    }

    let url = URL(fileURLWithPath: path)
    let handler = VNImageRequestHandler(url: url, options: [:])
    try handler.perform([request])

    let lines = (request.results ?? [])
        .compactMap { $0.topCandidates(1).first?.string }
    return lines.joined(separator: "\n")
}

let args = CommandLine.arguments.dropFirst()
if args.isEmpty {
    fputs("Usage: swift scripts/ocr_images.swift <image> [<image> ...]\n", stderr)
    exit(2)
}

var results: [OCRResult] = []
for path in args {
    do {
        results.append(OCRResult(imagePath: path, text: try recognize(path: path)))
    } catch {
        results.append(OCRResult(imagePath: path, text: "OCR_ERROR: \(error.localizedDescription)"))
    }
}

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
let data = try encoder.encode(results)
FileHandle.standardOutput.write(data)
FileHandle.standardOutput.write(Data("\n".utf8))
