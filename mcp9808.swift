/*
    Temperature readout using the I2CDriver Mini (https://i2cdriver.com/mini.html)
    and an MCP9808 digital temperature sensor (https://www.adafruit.com/product/1782)

    @version 1.0.1
*/

import Foundation
import Cocoa

class TemperatureReader: NSObject {
    // Basic class to process the call to the I2CDriver CLI process
    // and handle the necessary asynchronicity while reading back the
    // CLI's output


    // MARK: - Class Private Properties
    private var outputData: Data? = nil
    private var outputPipe: Pipe? = nil


    // MARK: - Class Public Functions
    func getReading() -> Float? {

        var result: Float? = nil
        let task: Process = Process()
        task.executableURL = URL.init(fileURLWithPath: "/usr/local/bin/i2ccl")
        task.arguments = ["/dev/cu.usbserial-DO029IEZ", "w", "0x18", "5", "r", "0x18", "2"]

        // Pipe out the output so we can trap it and extract the result
        outputPipe = Pipe()
        task.standardOutput = outputPipe
        let outFile = outputPipe!.fileHandleForReading
        outFile.waitForDataInBackgroundAndNotify()
        NotificationCenter.default.addObserver(self,
                                               selector: #selector(self.outputWriter),
                                               name: NSNotification.Name.NSFileHandleDataAvailable,
                                               object: nil)

        do {
            try task.run()
            // Pause until the process call is complete
            task.waitUntilExit()

            if task.terminationStatus == 0 {
                // CCL exited cleanly so process its output
                result = calculateResult()
            }
        } catch {
            // The CLI couldn't be run -- most likely it isn't installed
        }

        // Clean up and return
        NotificationCenter.default.removeObserver(self)
        self.outputData = nil
        return result
    }


    // MARK: - Class Private Functions
    @objc private func outputWriter(_ note: Notification) {
        // Async function called to stored piped text from the CLI call
        // to this process' data store
        if let pipe = self.outputPipe {
            let outHandle = pipe.fileHandleForReading
            if self.outputData == nil {
                self.outputData = Data()
            }

            // Write the standard output (via 'pipe') to the data store
            self.outputData!.append(outHandle.readDataToEndOfFile())
        }
    }


    private func calculateResult() -> Float {
        // Convert the output of the I2C process (a string) into float temperature
        // values then calculate the result, the final temperature value
        var result: Float = 9999.0
        if let data = self.outputData {
            if let outputString = String.init(data: data, encoding: String.Encoding.utf8) {
                // Typical i2ccl output is '0x42,0xaf' so remove the final character and split at the comma
                var parts = outputString.prefix(outputString.count - 1).split(separator: ",")
                parts[0] = parts[0].hasPrefix("0x") ? parts[0].dropFirst(2) : parts[0]
                parts[1] = parts[1].hasPrefix("0x") ? parts[1].dropFirst(2) : parts[1]

                // Get the reading bytes from the two hex strings
                let temp_lsb: Int = Int(String(parts[1]), radix: 16) ?? 0
                var temp_msb: Int = Int(String(parts[0]), radix: 16) ?? 0

                // Zero-out the MSB's status bits (see the MCP9808 data sheet)
                temp_msb = temp_msb & 0x1F

                if temp_msb & 0x10 == 0x10 {
                    // A negative temperature
                    temp_msb = temp_msb & 0x0F
                    result = 256.0 - (Float(temp_msb) * 16.0 + Float(temp_lsb) / 16.0)
                } else {
                    // A positive temperature
                    result = Float(temp_msb) * 16.0 + Float(temp_lsb) / 16.0
                }
            }
        }

        return result
    }
}


// MARK: - Main Entry Point

// Instantiate the class
let reader = TemperatureReader()

// Print a note for the user
print("Run started... hit CTRL-C to quit\n")

// Loop and take readings until Ctrl-C
while true {
    let temp = reader.getReading()
    if temp != nil {
        // Got a valid result so print it and pause for 5 seconds
        print(String(format: "Temperature: %.2fºC", temp!))
        do { sleep(5) }
    } else {
        // There was an error, so break to quit
        print("No reading")
        break
    }
}
