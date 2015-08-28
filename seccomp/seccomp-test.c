#include <stdio.h>
#include <unistd.h>
#include <seccomp.h>
#include <errno.h>
int main() {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ERRNO(EACCES));
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sigreturn), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 1,
		     SCMP_A0(SCMP_CMP_EQ, STDOUT_FILENO));
    /*
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 1,
		     SCMP_A0(SCMP_CMP_EQ, STDERR_FILENO));
    */

    puts("pre-load");
    seccomp_load(ctx);
    fprintf(stdout, "post-load (stdout)\n");
    fprintf(stderr, "post-load (stderr)\n");
    return 0;
}
