import re
from urllib.parse import urlsplit


__all__ = ['URLValidator']


class URLValidator:
    # Unicode letters range (must not be a raw string).
    ul = '\u00a1-\uffff'

    # IP patterns
    ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
    ipv6_re = r'\[[0-9a-f:.]+\]'  # (simple regex, validated later)

    # Host patterns
    hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'

    # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
    domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'

    tld_re = (
        r'\.'                                # dot
        r'(?!-)'                             # can't start with a dash
        r'(?:[a-z' + ul + '-]{2,63}'         # domain label
        r'|xn--[a-z0-9]{1,59})'              # or punycode label
        r'(?<!-)'                            # can't end with a dash
        r'\.?'                               # may have a trailing dot
    )

    host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'

    regex = re.compile(
        r'^(?:[a-z0-9.+-]*)://'  # scheme is validated separately
        r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'  # user:pass authentication
        r'(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')'
        r'(?::\d{2,5})?'  # port
        r'(?:[/?#][^\s]*)?'  # resource path
        r'\Z',
        re.IGNORECASE
    )

    schemes = ['http', 'https', 'ftp', 'ftps']

    def __init__(self, schemes=None, **kwargs):
        if schemes is not None:
            self.schemes = schemes

    def __call__(self, value, raise_exception=True):

        if not isinstance(value, str):
            if raise_exception is True:
                raise ValueError(
                    f"Expect str, received {type(value)}"
                )
            else:
                return False

        scheme = value.split('://')[0].lower()

        if scheme not in self.schemes:
            if raise_exception is True:
                raise ValueError(
                    f"Unknown scheme - {scheme}"
                )
            else:
                return False

        regex_matches = self.regex.search(value)

        if regex_matches is None:
            if raise_exception is True:
                raise ValueError(
                    "Provided value is not a valid URL"
                )
            else:
                return False

        # The maximum length of a full host name is 253 characters per RFC 1034
        # section 3.1. It's defined to be 255 bytes or less, but this includes
        # one byte for the length of the name and one byte for the trailing dot
        # that's used to indicate absolute names in DNS.
        if len(urlsplit(value).netloc) > 253:
            raise ValueError("netloc cannot be longer that 256 chars")

        return True
