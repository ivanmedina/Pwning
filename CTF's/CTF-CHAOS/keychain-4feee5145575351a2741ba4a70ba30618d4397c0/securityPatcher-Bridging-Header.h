//
//  Use this file to import your target's public headers that you would like to expose to Swift.
//

#include <xpc/xpc.h>

extern xpc_type_t _xpc_type_mach_send;
extern mach_port_t xpc_dictionary_copy_mach_send(xpc_object_t xdict, const char *key);

extern void csops(void);
extern void csops_audittoken(void);

/* code signing attributes of a process */
#define CS_VALID                    (uint32_t)0x00000001  /* dynamically valid */
#define CS_ADHOC                    (uint32_t)0x00000002  /* ad hoc signed */
#define CS_GET_TASK_ALLOW           (uint32_t)0x00000004  /* has get-task-allow entitlement */
#define CS_INSTALLER                (uint32_t)0x00000008  /* has installer entitlement */

#define CS_FORCED_LV                (uint32_t)0x00000010  /* Library Validation required by Hardened System Policy */
#define CS_INVALID_ALLOWED          (uint32_t)0x00000020  /* (macOS Only) Page invalidation allowed by task port policy */

#define CS_HARD                     (uint32_t)0x00000100  /* don't load invalid pages */
#define CS_KILL                     (uint32_t)0x00000200  /* kill process if it becomes invalid */
#define CS_CHECK_EXPIRATION         (uint32_t)0x00000400  /* force expiration checking */
#define CS_RESTRICT                 (uint32_t)0x00000800  /* tell dyld to treat restricted */

#define CS_ENFORCEMENT              (uint32_t)0x00001000  /* require enforcement */
#define CS_REQUIRE_LV               (uint32_t)0x00002000  /* require library validation */
#define CS_ENTITLEMENTS_VALIDATED   (uint32_t)0x00004000  /* code signature permits restricted entitlements */
#define CS_NVRAM_UNRESTRICTED       (uint32_t)0x00008000  /* has com.apple.rootless.restricted-nvram-variables.heritable entitlement */

#define CS_RUNTIME                  (uint32_t)0x00010000  /* Apply hardened runtime policies */

#define CS_ALLOWED_MACHO            (uint32_t)(CS_ADHOC | CS_HARD | CS_KILL | CS_CHECK_EXPIRATION | \
CS_RESTRICT | CS_ENFORCEMENT | CS_REQUIRE_LV | CS_RUNTIME)

#define CS_EXEC_SET_HARD            (uint32_t)0x00100000  /* set CS_HARD on any exec'ed process */
#define CS_EXEC_SET_KILL            (uint32_t)0x00200000  /* set CS_KILL on any exec'ed process */
#define CS_EXEC_SET_ENFORCEMENT     (uint32_t)0x00400000  /* set CS_ENFORCEMENT on any exec'ed process */
#define CS_EXEC_INHERIT_SIP         (uint32_t)0x00800000  /* set CS_INSTALLER on any exec'ed process */

#define CS_KILLED                   (uint32_t)0x01000000  /* was killed by kernel for invalidity */
#define CS_DYLD_PLATFORM            (uint32_t)0x02000000  /* dyld used to load this is a platform binary */
#define CS_PLATFORM_BINARY          (uint32_t)0x04000000  /* this is a platform binary */
#define CS_PLATFORM_PATH            (uint32_t)0x08000000  /* platform binary by the fact of path (osx only) */

#define CS_DEBUGGED                 (uint32_t)0x10000000  /* process is currently or has previously been debugged and allowed to run with invalid pages */
#define CS_SIGNED                   (uint32_t)0x20000000  /* process has a signature (may have gone invalid) */
#define CS_DEV_CODE                 (uint32_t)0x40000000  /* code is dev signed, cannot be loaded into prod signed code (will go away with rdar://problem/28322552) */
#define CS_DATAVAULT_CONTROLLER     (uint32_t)0x80000000  /* has Data Vault controller entitlement */

#define CS_ENTITLEMENT_FLAGS        (uint32_t)(CS_GET_TASK_ALLOW | CS_INSTALLER | CS_DATAVAULT_CONTROLLER | CS_NVRAM_UNRESTRICTED)
