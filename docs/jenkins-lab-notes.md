# Jenkins lab notes

## Decisions

- **The controller has 0 executors.** It only schedules jobs. Builds run on agents.
- **Builds run on a disposable agent with label `linux-build`.**
- **The Docker socket is mounted only on the agent, never on the controller.** Anyone who can run a job on that agent can control the host's Docker, so this is lab-only.

## Why not rootless builders (yet)

- Ubuntu 26.04 sets `kernel.apparmor_restrict_unprivileged_userns=1`.
- Rootless BuildKit and `rootlesskit` were blocked. A host AppArmor profile was tried but did not fix the child process.
- Left unsolved on purpose. We did not turn the restriction off.

## Real world

- Agents are ephemeral: a fresh VM or pod per job, deleted after.
- Images are built with rootless builders (BuildKit, Buildah) or on a managed runner.
- Only trusted pipelines can use agents with build access.
- Webhooks replace polling when Jenkins is reachable.
