### Create a systemd service file:
/etc/systemd/service/garden-lights.service

```text
[Unit]
Description=Scheduler to turn garden lights on / off
After=network.target

[Service]
User=<username>
WorkingDirectory=/<path>/garden_lights/app/
ExecStart=/<path>/.local/bin/gunicorn -b 0.0.0.0:8000 -w 4 'app:create_app()''
Restart=always

[Install]
WantedBy=multi-user.target
```

```text
# systemctl daemon-reload 
# systemctl start garden-lights.service
```

