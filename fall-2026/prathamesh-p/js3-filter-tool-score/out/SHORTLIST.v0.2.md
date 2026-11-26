# SHORTLIST: FILTER v0.2, every claim labelled against the posting text

- **Generated:** 2026-11-25 19:12:29 Eastern Standard Time by `python -I shortlist.py` from `out/decisions.all.v0.2.jsonl`. That file came from `python -I filter.py run --include-holdout --labels holdout/LABELS.json --out out/decisions.all.v0.2.jsonl`.
- **Population:** 1994 postings. **3 accepted, 0 flagged.** Ranked by FILTER R1.
- **Labels:** `supported` = a quoted sentence asserts the claim. `contradicted` = a quote asserts the opposite. `insufficient` = no quote either way, or a match without meaning.
- Every quote below was checked again as an exact substring of the stored posting (the result is printed per posting).
- **This is the filter's evidence, not a decision.** Whether a posting is worth the persona's time stays Prathamesh's call.

## 1. Network Engineer (openai, accept)

- **ID:** `9f78c41f-8d39-46c9-b9c3-c3b075905b24`. **Location (shown, not a claim):** San Francisco. **URL:** https://jobs.ashbyhq.com/openai/9f78c41f-8d39-46c9-b9c3-c3b075905b24
- **Quote check:** all quotes found again

| Claim | What is claimed | Label | Evidence (exact text) | Rule note |
|---|---|---|---|---|
| title | The job is network engineering work (SOC 15-1241) | **supported** | "Network Engineer" | network role title |
| authorization | Nothing in the posting excludes an F-1 holder who needs sponsorship | **insufficient** | (none) | A5: posting is silent on authorization and sponsorship |
| seniority | The level fits an entry-level candidate | **insufficient** | (none) | S4: no years and no level word stated |
| skills | The work uses at least 2 of the persona's networking skills | **supported** | **BGP**: "- Strong routing and switching fundamentals, including BGP, OSPF, VLAN/VRF design, WAN, Internet edge, and high-availability patterns."<br>**OSPF**: "- Strong routing and switching fundamentals, including BGP, OSPF, VLAN/VRF design, WAN, Internet edge, and high-availability patterns."<br>**VLAN**: "- Strong routing and switching fundamentals, including BGP, OSPF, VLAN/VRF design, WAN, Internet edge, and high-availability patterns."<br>**VPN**: "- Strong network security fundamentals, including ACLs, firewalls, VPN, 802.1X/NAC, device profiling, segmentation, and least privilege."<br>**firewall**: "- Implement and operate routing, switching, wireless, WAN, Internet edge, firewall, NAC, segmentation, and core network services."<br>**routing**: "- Implement and operate routing, switching, wireless, WAN, Internet edge, firewall, NAC, segmentation, and core network services."<br>**switching**: "- Implement and operate routing, switching, wireless, WAN, Internet edge, firewall, NAC, segmentation, and core network services." | K1: 7 networking terms: BGP, OSPF, VLAN, VPN, firewall, routing, switching |

## 2. Network Infrastructure Engineer, Global Network Infra (WAN) (openai, accept)

- **ID:** `9f7371c4-e306-4a45-a400-aa2843fabd85`. **Location (shown, not a claim):** San Francisco. **URL:** https://jobs.ashbyhq.com/openai/9f7371c4-e306-4a45-a400-aa2843fabd85
- **Quote check:** all quotes found again

| Claim | What is claimed | Label | Evidence (exact text) | Rule note |
|---|---|---|---|---|
| title | The job is network engineering work (SOC 15-1241) | **supported** | "Network Infrastructure Engineer, Global Network Infra (WAN)" | network role title |
| authorization | Nothing in the posting excludes an F-1 holder who needs sponsorship | **insufficient** | (none) | A5: posting is silent on authorization and sponsorship |
| seniority | The level fits an entry-level candidate | **insufficient** | (none) | S4: no years and no level word stated |
| skills | The work uses at least 2 of the persona's networking skills | **supported** | **BGP**: "- Have a strong understanding of networking fundamentals, including optical networking, Ethernet, TCP/IP, BGP, and Layer 2/3 connectivity."<br>**TCP/IP**: "- Have a strong understanding of networking fundamentals, including optical networking, Ethernet, TCP/IP, BGP, and Layer 2/3 connectivity."<br>**routing**: "- Troubleshoot complex network issues across physical, Layer 2, and Layer 3 infrastructure, including optical signal problems, FEC errors, routing issues, and connectivity failures." | K1: 3 networking terms: BGP, TCP/IP, routing |

## 3. Network Engineer (openai, accept)

- **ID:** `a80e213f-c592-4337-a410-e5bf94f4e40d`. **Location (shown, not a claim):** London, UK. **URL:** https://jobs.ashbyhq.com/openai/a80e213f-c592-4337-a410-e5bf94f4e40d
- **Quote check:** all quotes found again

| Claim | What is claimed | Label | Evidence (exact text) | Rule note |
|---|---|---|---|---|
| title | The job is network engineering work (SOC 15-1241) | **supported** | "Network Engineer" | network role title |
| authorization | Nothing in the posting excludes an F-1 holder who needs sponsorship | **insufficient** | (none) | A5: posting is silent on authorization and sponsorship |
| seniority | The level fits an entry-level candidate | **insufficient** | (none) | S4: no years and no level word stated |
| skills | The work uses at least 2 of the persona's networking skills | **supported** | **routing**: "- End-to-end ownership of secure enterprise routing, switching, wireless, WAN, network services, and cloud connectivity."<br>**switching**: "- End-to-end ownership of secure enterprise routing, switching, wireless, WAN, network services, and cloud connectivity." | K1: 2 networking terms: routing, switching |
