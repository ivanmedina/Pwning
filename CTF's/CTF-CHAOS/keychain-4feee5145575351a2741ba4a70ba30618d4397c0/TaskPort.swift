//
//  TaskPort.swift
//  securityPatcher
//
//  Created by Linus Henze.
//  Copyright © 2019 Linus Henze. All rights reserved.
//

import Foundation

class TaskPortError: Error, CustomStringConvertible {
    var description: String
    
    init(_ error: kern_return_t) {
        description = "Error: \(String(cString: mach_error_string(error)))"
    }
}

//
// NOTE: This is not the real implementation.
//       You *must* disable SIP to try this.
//
//       P.S. We're not stupid. SIP is enabled on our VM.
//
func getTaskPort(pid: pid_t) throws -> mach_port_t {
    var tp: mach_port_t = 0
    let kr = task_for_pid(mach_task_self_, pid, &tp)
    if kr != KERN_SUCCESS {
        throw TaskPortError(kr)
    }
    
    return tp
}

func setCSFlags(pid: pid_t, flags: UInt32) throws {
    // Not implemented in public version.
    // On your machine, you might get prompts that "only Apple software may use the Security Agent"
    // due to the code signature being broken after patching
    // (this function, if implemented, would "restore" the code signature).
    // These prompts won't appear when your exploit is successful.
}

func disableTaskPortAccess() throws {
    // Disables our internal task port backdoor that we use for patching instead of task_for_pid.
    // Don't kill securityd!
    // It will restart unpatched and rerunning this tool on the VM won't work!
}
