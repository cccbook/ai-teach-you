// IP 封包結構

struct iphdr {
    unsigned char  ihl:4, version:4;
    unsigned char  tos;
    unsigned short tot_len;
    unsigned short id;
    unsigned short frag_off;
    unsigned char  ttl;
    unsigned char  protocol;
    unsigned short check;
    unsigned int   saddr;
    unsigned int   daddr;
    // options...
};

// TCP 標頭
struct tcphdr {
    unsigned short source;
    unsigned short dest;
    unsigned int   seq;
    unsigned int   ack;
    unsigned char  data_off:4, reserved:4;
    unsigned char  flags;
    unsigned short window;
    unsigned short check;
    unsigned short urgent;
};

// UDP 標頭
struct udphdr {
    unsigned short source;
    unsigned short dest;
    unsigned short len;
    unsigned short check;
};
