# Tested (full negatives ledger)

The summary table in the folder's `README.md` shows the highlights; this file is the
complete record. Add one row per hypothesis family tested, in the order tested. Never remove
a row; if a hypothesis is retested with a different method, add a new row rather than editing
the old one.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 1, families A to D: the literal readings of the two 2026-08-28 hints (raw keys from windows of the coinbase text, BIP32 seeds and BIP39 entropy from the same text along 214 paths including every BIP48 path with a genesis integer as account, the other genesis fields), every ordered pair of the union | 447,916 distinct public keys (447,922 records with 6 witness copies), 200,634,118,084 ordered pairs | keys generated on the CPU by `tools/candidates.py` (22 processes, 15 s), pairs formed and hashed on the GPU by `engines/p2wsh_2of2_pairs.cu`, exact 32-byte compare with the escrow program; every GPU hit re-derived on the CPU with `tools/oracle.py` | 0 match | yes: the 2-of-2 pair revealed in block 963,629 placed at head, middle and tail of the key file, all 9 ordered combinations re-found, engine reported `exhausted=yes` | 1.95e9 ordered pairs/s on one RTX 5080, 103 s | 2026-08-29 |
| Pass 2, families A to D plus E (hashed roots: SHA-256, double SHA-256, hash160, SHA-512 of each text as raw key, BIP32 seed and BIP39 entropy), F (raw extended key: 32 key bytes plus 32 chain-code bytes taken from the text, swapped and reversed forms), G (raw key with a zero chain code for the 16 to 32-byte windows of the text, the texts modulo n, the genesis integers and the fields), all along the same 214 paths, every ordered pair of the union | 611,008 distinct public keys (611,014 records with 6 witness copies), 373,338,108,196 ordered pairs | same pipeline as pass 1 with `tools/candidates.py --pass 2` (22 processes, 17 s) | 0 match | yes: same witness pair at head, middle and tail, all 9 ordered combinations re-found, `exhausted=yes` | 4.18e9 ordered pairs/s on one RTX 5080, 89 s | 2026-08-29 |

## Pass 2 in full

373,338,108,196 ordered pairs tested, 0 match. Method: the pass 1 key set plus 165,064 keys
from three more families (16,548 E, 2,996 F, 145,306 G before deduplication), 611,008 distinct
public keys in total, every ordered pair rebuilt as the 2-of-2 witness script, hashed on the GPU
and compared byte for byte with the escrow's witness program. Witness: same protocol as pass 1,
9 of 9 ordered head/middle/tail combinations re-found and confirmed on the CPU, no other hit.
Rate: 4.18e9 ordered pairs/s on one RTX 5080, 89 s elapsed. Date: 2026-08-29.

Scope added by pass 2 (labels E:, F:, G: in `labels.tsv`):

- E, hashed roots despite "no hash": SHA-256, double SHA-256, hash160 and SHA-512 of each of
  the 7 texts, each used (1) as a raw private key (first 32 bytes big-endian and reversed; for
  SHA-512 also the second half and the whole digest modulo n), (2) as a BIP32 seed, (3) as
  BIP39 entropy of 32 and 16 bytes with an empty passphrase, then the 214 paths. 70 integers,
  77 seeds.
- F, raw extended key: master private key = X[:32] and chain code = X[32:64] for X in T, S,
  the lower and upper-case forms of T, and the byte-reversed T and S, plus the two halves
  swapped, plus T[:32] with T[37:69] and its swap, then the 214 paths. 14 roots.
- G, raw private key imported with a zero chain code: every 16/20/24/28/32-byte window of T
  read big-endian, little-endian and right-padded, T, J and S modulo n, the 12 genesis
  integers, and the fields of at most 32 bytes, then the 214 paths. 680 roots.

After pass 2 the mechanical readings of "root -> multisig -> mainnet -> genesis_data ->
script_type" with the coinbase text as the source are closed on this list of paths. Still not
covered: SLIP-39, BIP85, a passphrase other than empty or T, paths outside the 214, and a
witness script other than `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG` with compressed keys.

## Pass 1 in full

200,634,118,084 ordered pairs tested, 0 match. Method: 447,916 distinct public keys built on
the CPU from four families, then every ordered pair (i, j) rebuilt as
`OP_2 <Ki> <Kj> OP_2 OP_CHECKMULTISIG`, hashed with SHA-256 on the GPU and compared byte for
byte with the escrow's witness program. Witness: the real 2-of-2 pair spent in block 963,629
(transaction `47ded3504e855ce418e46eeca4694b55a623d1e23a8e3c83292abbcf9cee9f7a`) inserted at
the head, the middle and the tail of the key file with its own program as a second target; all
9 ordered head/middle/tail combinations were re-found and confirmed on the CPU, and no other
hit appeared. Rate: 1.95e9 ordered pairs/s on one RTX 5080, 103 s elapsed. Date: 2026-08-29.

Exact scope of the key set (labels in `labels.tsv` produced by `tools/candidates.py --write`):

- A, raw private keys: every 1 to 32-byte window of the 69-byte coinbase text T, the 47-byte
  headline J, the 77-byte scriptSig S and the lower and upper-case forms of T and J, read as a
  big-endian integer, a little-endian integer and right-padded to 32 bytes; windows longer
  than 32 bytes reduced modulo the curve order (big and little-endian); the 12 genesis
  integers {0, 1, 2, 3, 9, 50, 2009, 3012009, 20090103, 1231006505, 2083236893, 486604799};
  the other fields (D). Compressed keys, plus uncompressed keys for T, J, S, the integers and
  the fields. 36,816 integers, 54,264 keys before deduplication.
- B, BIP32 seeds: each whole text, its 16/20/24/28/32/64-byte windows, T[32:], T[22:] and the
  fields of at least 16 bytes (1,370 seeds), each derived along 214 paths: `m/48'/0'/a'`,
  `m/48'/0'/a'/s'`, `m/48'/0'/a'/s'/0/0`, `/0/1`, `/1/0` and `m/48/0/a/s/0/0` for every
  genesis integer a and script type s in {0, 1, 2}; `m`, `m/0`, `m/0/0`, `m/0/1`, `m/1/0`,
  `m/0'`, `m/0'/0`, `m/0'/0'`, `m/0'/0'/0'`, `m/44'/0'/0'/0/0`, `m/44'/0'/0'/0/1`,
  `m/44'/0'/0'`, `m/49'/0'/0'/0/0`, `m/84'/0'/0'/0/0`, `m/84'/0'/0'/0/1`, `m/86'/0'/0'/0/0`,
  `m/45'`, `m/45'/0/0`, `m/45'/0/0/0`, `m/45'/1/0/0`, `m/48'`, `m/48'/0'`. 293,180 keys.
- C, BIP39 entropy: the 16/20/24/28/32-byte windows of the same texts and the prefixes of the
  32-byte fields, English mnemonic, seed with an empty passphrase and with T as passphrase
  (2,730 seeds), same 214 paths. 584,220 keys.
- D, other fields as raw keys: merkle root (both byte orders), block hash (both), coinbase
  public key and its x and y coordinates, header, coinbase transaction, nonce, time, bits and
  version (both byte orders). 90 keys.

The union deduplicates to 447,916 keys because J is a suffix of T, T is a suffix of S, and the
case-changed forms share every window without a letter.

What this negative does not cover: a root built by a library step not modeled here (a raw
private key with a zero chain code, a raw extended key made of 32 key bytes plus 32 chain-code
bytes, BIP85, SLIP-39), hashed roots (the author said "no hash", but a SHA-256 of the text as
seed or key costs nothing to add), paths outside the list above, a passphrase other than empty
or T, and any witness script other than `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG` with 33-byte keys
(uncompressed keys were only tried for family A and D).


## Additional bounded constructions, 2026-09-05 (contributed by @BorisLoveDev, PR #21)

Recorded escrow check on 2026-09-05: 142,779 sats, 18 funded outputs, none spent; no pending transactions. No newer message at the escrow or the last author change address. All tests below passed the existing oracle self-test before generation and compared the exact 32-byte target witness program. Candidate material stayed local; no transactions were constructed or sent.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| T and J exact/lower/upper directly as BIP39 mnemonic sentences, PBKDF2 with empty passphrase, existing 214 paths | 1,284 unique compressed keys; 1,648,656 candidate ordered pairs; 1,664,100 stream pairs including witness-key cross-pairs | CPU SHA256 of standard 2-of-2 script, exact target-program comparison | 0 match, exhausted | real revealed pair at head/middle/tail of key records, all 9 combinations recovered; BIP39 PBKDF2 also checked against a valid mnemonic vector | 2.62M hashes/s calibration; 0.873 s total | 2026-09-05 |
| Newspaper date as decimal YYYYMMDD/DDMMYYYY/MMDDYYYY integer, BE/LE padded to 16/32 bytes, BIP32 seed or BIP39 entropy with empty passphrase, existing 214 paths | 5,136 unique keys; 26,378,496 candidate ordered pairs; 26,440,164 stream pairs including witness-key cross-pairs | same exact CPU checker | 0 match, exhausted | same real pair inserted head/middle/tail, all 9 combinations recovered | 2.72M hashes/s calibration; 11.548 s total | 2026-09-05 |
| T[:21] exact/lower/upper directly as BIP39 mnemonic, empty passphrase, 214 paths; paired with itself and prior direct-mnemonic keys | 642 new keys plus 1,284 old keys; 2,060,820 new ordered pairs, old-old pairs excluded | exact CPU checker; 3 additional witness pair records | 0 match, exhausted | real pair recovered at stream head/middle/tail | 2.48M hashes/s calibration; 2.366 s total | 2026-09-05 |
| T/J/T[:21] as hardened byte indices or 4-byte BE chunk indices inside m/48'/0'/text/2', optional /0/0; seed T or 32 zero bytes | 24 keys, 576 ordered pairs | exact CPU checker; final chunk padded right with zero, chunks masked to 31 bits; 3 additional witness records | 0 match, exhausted | real pair recovered at stream head/middle/tail | 2.90M hashes/s calibration; 0.027 s total | 2026-09-05 |

These negatives cover only the stated constructions and paths. They do not establish that any natural-language clue has a unique interpretation.


| Additional hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Zero-filled 16/32 bytes as BIP32 seed or BIP39 entropy, empty passphrase, prior 214 paths | 856 keys; 732736 candidate ordered pairs, 743044 stream pairs including witness-key cross-pairs | standard 2-of-2 script, exact target SHA256 compare | 0 match, exhausted | public real pair at head/middle/tail, all 9 combinations recovered; oracle self-test passed | 2.83M hashes/s calibration; 0.434 s total | 2026-09-05 |
| Six canonical T/J raw BIP32 seeds, all hardening combinations for 48/0/account/script, prior 12 genesis accounts, script 0/1/2, suffix empty or /0/0 /0/1 /1/0; pairs share a hardening pattern | 11150784 new ordered pairs in 15 patterns; all prior old-old pairs excluded; standard all-hardened group had no new pairs and was skipped | exact CPU target-program compare | 0 match, exhausted | public real pair at stream head/middle/tail, all 3 recovered; oracle self-test passed | 2.47M hashes/s calibration; 8.625 s total | 2026-09-05 |


[Scripts and per-run reports](../tools/REPRODUCE.md) preserve the six bounded
constructions. The pair counts above are per-family coverage, not a claim that
all families are mutually disjoint. No solution was obtained.

## Pass 3, the September model (2026-09-12)

After the author's answers of 2026-09-10 and 2026-09-11 (12 words, a passphrase, entropy from the genesis block, a genesis value as the BIP48 account), one bounded pass over that model.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Pass 3, the September model (2026-09-12): 12-word BIP39 mnemonic whose entropy is a 16-byte window of genesis data (every window of the raw 285-byte block, of the merkle root and block hash in both byte orders, of the coinbase text, headline, scriptSig, header and coinbase public key, plus the header integers zero-padded and as decimal strings: 329 entropies), 53 passphrases (empty as control, the coinbase text, the headline, The Times, Satoshi, genesis, bitcoin, the header integers, the hashes in hex and a dozen short words from the author's messages), BIP48 `m/48'/0'/a'/s'` with a in {0, 1, 2, 3, 50, 2009, 285, bits, time, nonce} and s in {0', 1', 2'}, suffix empty, /0/0 or /0/1; every ordered pair | 1,569,330 keys, 2.463e12 ordered pairs | CPU BIP39/BIP32 generation (25 s on 22 cores), GPU pairing and SHA-256 (`engines/p2wsh_2of2_pairs.cu`, 4.18e9 pairs/s, 589 s), exact 32-byte compare | 0 match | yes: revealed 2-of-2 pair at head, middle and tail, 9 of 9 ordered combinations re-found, `exhausted=yes` | 2026-09-12 |

Scope: only 12-word mnemonics, only the listed entropy windows, only the 53 listed passphrases, only the listed accounts and script types, compressed keys. Under that model the passphrase is not among the obvious readings of the block. Not covered: a passphrase outside the list (the one thing the author has not described), 24 words, other accounts, non-BIP48 paths.

## Pass 4, the digest model, wave 1 (2026-09-17)

The author's answers of 2026-09-14 to 2026-09-17 replace the raw-window model that pass 3
tested: the entropy "isn't the raw 16 bytes", it is "a 128-bit digest"; the passphrase "is a
name", the name of whoever received the first transaction, in a format the author says has to
be found by brute force; the 12 words "were generated from entropy"; the wallet was built with
"the tools that support BIPs 32, 39, and 48". Wave 1 tests that model with both cosigner keys
coming from one seed and differing by BIP48 path.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 4 wave 1: entropy = a 128-bit digest of genesis data (18 digest readings, md5 plus the 128-bit truncations of sha1, sha224, sha256, sha256d, sha512, ripemd160, hash160, sha3-256, blake2b, blake2s and shake-128, over 73 genesis inputs: the coinbase text, headline, scriptSig, raw block, header, coinbase transaction, public key, merkle root and block hash in both byte orders, the coinbase address, the header integers, each also as lower and upper-case hex; 1,278 distinct entropies), 12-word BIP39 mnemonic, passphrase = one of 47 name formats for Hal Finney, Harold Finney and Satoshi Nakamoto, BIP48 `m/48'/0'/a'/s'` with a in {0, 1, 2, 3, 50, 170, 285, 2009, 20090103, 3012009, time, nonce, bits} and s in {0', 1', 2'}, suffix empty, /0/0, /0/1 or /1/0; both keys from the same seed, every ordered pair inside each seed | 60,066 seeds, 9,370,296 keys, 1,452,484,146 ordered pairs | CPU BIP39/BIP32 generation and pairing, `tools/check_digest_model.py --wave 1`, 8 processes, exact 32-byte compare against the escrow witness program | 0 match | yes: the revealed 2-of-2 pair of block 963,629 inserted in the first, middle and last entropy group, re-found 141 of 141 times (3 groups x 47 passphrases, one valid key order each) | 2,873,073 ordered pairs/s on an 8-core Apple M-series CPU, 506 s | 2026-09-17 |

Scope: only 12-word mnemonics, only the 1,278 listed digests, only the 47 listed name formats,
only the listed BIP48 accounts and script types, compressed keys, both keys from one seed. Not
covered by this wave: two keys from two different digests (wave 2 below), a digest input not in
the list of 73, a name format outside the 47, and any digest of a file rather than of the
genesis data itself.

## Pass 4, the digest model, wave 2 (2026-09-17)

Wave 1 assumed both cosigner keys come from one seed. Wave 2 covers the other reading of
"both keys are derived independently from Genesis": two different 128-bit digests, two
mnemonics, the same name passphrase and the same path, which is how two cosigners of one
BIP48 multisig wallet are normally set up. The author answered "Perhaps" when asked whether
both cosigners share the words and the passphrase, so neither reading can be dropped.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 4 wave 2: the same 1,278 digest entropies and 47 name formats as wave 1, keys taken at 65 paths (`m/48'/0'/a'/s'/0/0` for the 13 genesis accounts and s in {0', 1', 2'}, plus `/0/1` and `/1/0` at s = 2'), every ordered pair of two different entropies at the same path under the same passphrase | 3,904,290 keys, 4,986,775,560 ordered pairs | CPU BIP39/BIP32 generation and pairing, `tools/check_digest_model.py --wave 2`, 8 processes, exact 32-byte compare | 0 match | yes: the revealed pair of block 963,629 inserted at the first, middle and last passphrase, re-found 195 of 195 times (3 passphrases x 65 paths, one valid key order each) | 4,774,535 ordered pairs/s on an 8-core Apple M-series CPU, 1,044 s | 2026-09-17 |

Waves 1 and 2 together test 6,439,259,706 ordered pairs of the digest model and match nothing.
What this does not cover: a digest input outside the 73 listed (the unanswered on-chain
question of 2026-09-17 asks the author exactly this: typed text, raw block bytes, a file, or
something else), a name format outside the 47, a digest algorithm outside the 18, mixing two
different passphrases or two different paths across the two cosigners, and 24-word mnemonics.

## Pass 4, wave 3: typed inputs and the cross-passphrase pair (2026-09-17)

Waves 1 and 2 hashed the canonical genesis bytes. The author's pending question offers "typed
text" as the first option for the digest input, and the 2026-08-28 hint says a solver can work
from The Times rather than from the block, so wave 3 hashes what a person types instead: case
forms, collapsed spacing, a trailing newline, CRLF, period or space, surrounding quotes, eight
ways of writing the date, and the block as a hex file with and without a trailing newline. It
also widens the name formats to 137 and adds the pairing waves 1 and 2 do not cover, two
different formats of the same name under one entropy, which is what the author's "Perhaps"
leaves open.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 4 wave 3: 300 typed inputs under 16 digest readings (4,800 distinct entropies), 137 name formats, 36 paths (`m/48'/0'/a'/2'/0/0`, `/0/1` and `m/48'/0'/a'/1'/0/0` for 12 genesis accounts); scheme A pairs two paths under one seed, scheme B pairs two name formats of the same name under one entropy at the 24 native-P2WSH paths | 4,800 entropies, 1,591,661,238 ordered pairs | CPU generation and pairing, `tools/check_digest_model.py --wave 3`, 8 processes, exact 32-byte compare | 0 match | yes: the revealed pair of block 963,629 inserted in the first, middle and last entropy group, re-found 3 of 3 | 1,011,953 ordered pairs/s on an 8-core Apple M-series CPU, 1,573 s | 2026-09-17 |

Scope: the 300 listed typed forms only, 16 of the 18 digest readings (the two byte-offset
RIPEMD readings were covered over the canonical inputs in waves 1 and 2), 137 name formats,
12 accounts, script types 1' and 2'. The three waves together test 8,030,920,944 ordered pairs
of the digest model. The digest input remains the open unknown, and buying it from the author
is still the cheapest way to close it.

## Pass 4, wave 4: the four forms (2026-09-17)

On 2026-09-17 23:22 UTC, in block 967,477, the author answered the question about the digest
input with the first statement about how that input is written: "The genesis block data can be
viewed in binary, hex, decimal, or ASCII. If you figure out which part is being used as the
entropy, just try all four forms." Wave 4 applies that rule to every part of the block I can
name.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 4 wave 4: 25 genesis parts (version, previous hash, merkle root, time, bits and nonce in both byte orders, the block hash in both orders, the header, the whole block, the coinbase transaction, the coinbase text, the headline, the scriptSig, the public key and its two coordinates, the 16-byte prefixes of the two hashes, the block reward), each rendered in 11 forms covering the author's four views (raw bytes, lower-case hex, upper-case hex, the decimal value of the field, the bit string plain, with leading zeros stripped and byte-spaced, the latin-1 ASCII view, the dotted printable view, and the per-byte decimal lists space and comma separated), each form hashed under 16 digest readings; 12-word BIP39, 47 name formats, 52 paths (13 genesis accounts, script types 0', 1', 2', suffixes /0/0 and /0/1); phase A pairs two paths inside one seed, phase B pairs two entropies at the 13 native-P2WSH `/0/0` paths under one passphrase | 275 forms, 4,284 distinct entropies, 11,744,847,956 ordered pairs | CPU BIP39/BIP32 generation and pairing, `tools/check_digest_model.py --wave 4`, 8 processes, exact 32-byte compare | 0 match | yes: the revealed 2-of-2 pair of block 963,629 inserted in the first, middle and last entropy group of phase A and in the first column of phase B, 4 of 4 re-found | 2,056,087 ordered pairs/s on an 8-core Apple M-series CPU, 5,712 s | 2026-09-17 |

Scope: the 25 parts listed and no others, the 11 renderings listed, 16 digest readings, 47 name
formats, 52 paths. The author's rule is about the form, not the part, and "which part is being
used" stays open: a part can be smaller or larger than a field, and wave 4 does not enumerate
windows of the block, the individual fields of the coinbase transaction, or the pieces of the
scriptSig. The four passes together test 605,494,412,466 ordered pairs of this puzzle.

## Pass 4, wave 5: more parts, cosigners from one part (2026-09-17)

Wave 4 took the parts a person names when reading a block header. Wave 5 takes the parts a
person names when reading the block's bytes: the fields of the coinbase transaction, the pieces
of its scriptSig and of its output script, and windows of the block and of the text. It also
narrows the cross pairing to what the author said on 2026-08-24, "both keys use the same Genesis
field": phase B pairs two entropies only when both come from the same part, two forms or two
digests of one field, rather than across unrelated parts as waves 2 and 4 did.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 4 wave 5: 19 structural parts (coinbase transaction version, input count, prevout hash, prevout index, script length, scriptSig, sequence, output count, the 5,000,000,000-sat value and its decimal string, output script, locktime; the scriptSig pieces `04ffff001d`, `ffff001d`, `0104`, the length byte `45` and the text; the output script framing `41` and `ac`) in all 11 renderings of the four forms, plus 114 window parts (every 16-byte window of the 285-byte block at stride 4, every 32-byte window at stride 8, every 16-byte window of the coinbase text at stride 4) in the four core renderings; 16 digest readings, 10,908 entropies, 47 name formats, 52 paths; phase A pairs two paths inside one seed, phase B pairs two entropies of the same part at 13 native-P2WSH paths under the first 24 name formats | 133 parts, 10,908 entropies, 1,666,960,548 ordered pairs | CPU generation and pairing, `tools/check_digest_model.py --wave 5`, 8 processes, exact 32-byte compare | 0 match | yes: the revealed pair of block 963,629 inserted in the first, middle and last structural part, in both phases, 6 of 6 re-found | 1,163,169 ordered pairs/s on an 8-core Apple M-series CPU, 1,433 s | 2026-09-17 |

Scope: the 19 structural parts and the 114 windows listed, at those strides. Windows at stride 1,
windows of lengths other than 16 and 32, the fields of the block as an explorer renders them in
JSON, and digest functions outside the 16 are not covered. Five passes now test 607,161,373,014
ordered pairs of this puzzle.

## Pass 4, wave 6: the digest function and the key encoding (2026-09-18)

Waves 1 to 5 varied the input. Wave 6 varies the two things they all held fixed. First, "a
128-bit digest" had been read as MD5 or a truncation of the SHA family; MD4 and MD2 are
natively 128 bits and were never tried, and Keccak-256 is a different function from SHA3-256,
which matters because any tool that calls its hash "sha3" gives Keccak. Second, every witness
script had been built with 33-byte compressed keys, while a P2WSH program commits only to the
hash of the script, so 65-byte uncompressed keys are equally valid inside it; this folder had
listed that gap since pass 1.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 4 wave 6: eight further digest readings (MD4, MD2, the two halves of Keccak-256, two of Keccak-512, two of SM3) over 44 structural parts in all 11 renderings of the four forms, 2,584 new entropies; plus the 4,284 wave-4 entropies re-derived with both key encodings, every ordered pair of compressed and uncompressed keys inside each seed, and two entropies of the same part paired at the native-P2WSH paths | 6,868 entropies, 3,573,791,110 ordered pairs | CPU generation and pairing, `tools/check_digest_model.py --wave 6`, 8 processes, exact 32-byte compare | 0 match | yes: the revealed pair of block 963,629 inserted in the first, middle and last new-digest entropy, 3 of 3 re-found | 2,339,947 ordered pairs/s on an 8-core Apple M-series CPU, 1,527 s | 2026-09-18 |

Scope: the eight listed digest readings and the two key encodings, over the structural parts
only; the 114 window parts of wave 5 were not re-run under the new digests or the uncompressed
encoding. RIPEMD-128 and Whirlpool, both 128-bit and both plausible, are not available in this
environment and remain untested. Six passes now test 610,735,164,124 ordered pairs of this
puzzle, and no reading of the entropy input, the digest function, the passphrase format or the
key encoding tried so far reproduces the escrow.
