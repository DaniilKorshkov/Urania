import bluetooth

print(bluetooth.discover_devices(duration=8, flush_cache=True, lookup_names=False, lookup_class=False, device_id=-1, iac=10390323))