# Kraken
###
**Multi-Target Multi thread DDoS Script Using Sequential URL Requests to multiple targets and Rotating Proxies/User Agents**

---

### **Breakdown**:

1. **Sequential Numeric IDs**:
   - The script targets URLs structured as `https://hackerone.com/reports/{id}`, where `{id}` ranges from `0000001` to `9999999`. It systematically generates requests to these URLs.

2. **Concurrent Requests**:
   - The script uses `concurrent.futures.ThreadPoolExecutor` to handle multiple requests at the same time. This ensures a high volume of simultaneous requests, which can overwhelm a server.
   - By default, the script runs 50 threads concurrently, making it highly effective for stress testing.

3. **Rotating User Agents**:
   - A set of 10 different user agents is used, with each request randomly selecting one. This prevents easy detection and blocking of requests based on user-agent strings.

4. **Proxy Usage**:
   - The script supports the use of a proxy list. If provided, proxies are rotated randomly with each request, making it harder to block based on IP addresses.

5. **Additional URL Targets**:
   - In addition to the primary report URLs, the script also makes GET requests to other specified URLs, including LinkedIn and Bitly links, adding more diversity to the attack pattern.

---

### **How to Run the Script**:

1. **Without Proxies**:
   ```bash
   python3 script_name.py --start 1 --end 9999999 --delay 0.00001 --concurrency 50
   ```

2. **With Proxies**:
   ```bash
   python3 script_name.py --start 1 --end 9999999 --delay 0.00001 --concurrency 50 --proxies list.txt
   ```

---

### **What It Does**:
- **Simultaneously sends requests** to a sequence of report URLs and additional specified URLs.
- **Randomizes user agents** to avoid detection and blocking.
- **Uses optional proxies** to obfuscate the origin of the requests.
- **Operates concurrently**, sending multiple requests at once, potentially leading to resource exhaustion on the targeted servers.

![Kraken hitting Hackerone ](https://raw.githubusercontent.com/DeadmanXXXII/Kraken/main/Screenshot_20240816-100715.png)


