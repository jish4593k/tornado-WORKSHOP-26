import asyncio

async def execute_command_async(command, timeout):
    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.gather(
            proc.stdout.read(),
            proc.stderr.read(),
        )

        await proc.wait()
        return (await proc.communicate(), False)
    except asyncio.TimeoutError:
        return (b"", b"Timed out", True)

async def main():
    tasks = []
    tasks.append(execute_command_async("sleep 5", 3))
    tasks.append(execute_command_async("sleep 1", 3))
    tasks.append(execute_command_async("invalid_command", 3))
    tasks.append(execute_command_async("cat /etc/hosts", 3))

    results = await asyncio.gather(*tasks)

    for (stdout, stderr, timed_out) in results:
        status = 1 if timed_out else 0
        if not timed_out:
            print(f"Process completed successfully: status={status}, stdout={stdout}, stderr={stderr}")
        else:
            print(f"Process timed out: status={status}, stdout={stdout}, stderr={stderr}")

if __name__ == "__main__":
    asyncio.run(main())
