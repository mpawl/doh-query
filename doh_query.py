import argparse
import base64
import dns.message
import dns.rdatatype
import httpx
import sys

def encode_dns_query(domain, qtype):
    query = dns.message.make_query(domain, qtype)
    wire = query.to_wire()
    return base64.urlsafe_b64encode(wire).rstrip(b'=').decode()

def perform_doh_query(responder, encoded_query):
    url = f"https://{responder}/dns-query?dns={encoded_query}"
    headers = {
        'Accept': 'application/dns-message'
    }
    with httpx.Client(http2=True, headers=headers, timeout=10) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.content

def format_short(rr):
    # Return a short representation of a resource record
    if hasattr(rr, 'address'):  # A, AAAA
        return rr.address
    if hasattr(rr, 'target'):  # CNAME, NS, PTR
        return rr.target.to_text()
    if hasattr(rr, 'strings'):  # TXT
        return ' '.join(s.decode('utf-8') for s in rr.strings)
    if hasattr(rr, 'exchange'):  # MX
        return rr.exchange.to_text()
    if hasattr(rr, 'rdtype') and rr.rdtype == dns.rdatatype.SOA:
        return f"{rr.mname} {rr.rname} {rr.serial}"
    # Default: return full string representation
    return rr.to_text()

def parse_dns_response(response_wire, short_output):
    msg = dns.message.from_wire(response_wire)

    if short_output:
        for rrset in msg.answer:
            for rr in rrset:
                print(format_short(rr))
    else:
        # Make it look like dig anser
        print(";; ANSWER SECTION:")
        for rrset in msg.answer:
            print(rrset.to_text())

def main():
    # Place args here
    parser = argparse.ArgumentParser(description='Perform DoH query via Apple DNS')
    parser.add_argument('-n', '--name', required=True, help='Hostname to resolve')
    parser.add_argument('-r', '--responder', default='cloudflare-dns.com', help='Responder to use (default: cloudflare-dns.com)')
    parser.add_argument('-t', '--type', default='A', help='DNS record type (default: A)')
    parser.add_argument('-s', '--short', action='store_true', help='Mimic dig +short output')
    args = parser.parse_args()

    try:
        qtype = dns.rdatatype.from_text(args.type.upper())
    except Exception as e:
        print(f"Invalid query type '{args.type}': {e}")
        sys.exit(1)

    encoded_query = encode_dns_query(args.name, qtype)
    try:
        raw_response = perform_doh_query(args.responder, encoded_query)
        parse_dns_response(raw_response, args.short)
    except httpx.HTTPError as e:
        print(f"HTTP error during DoH request: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(3)

if __name__ == '__main__':
    main()

