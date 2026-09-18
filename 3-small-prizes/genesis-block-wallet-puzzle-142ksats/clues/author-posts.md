# Author posts, verbatim

Every message of this puzzle is an OP_RETURN output in a transaction that also pays the
escrow `bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj`. The author has no
other channel. The attribution below follows the transaction inputs: a message is the
author's when its inputs spend a change output of a previous author transaction (the
announcement is the anchor). Questions paid directly to an author change address were
re-posted by the author to the escrow before the answer; those re-posts are marked
"relayed". All times are UTC, read from the block timestamps on 2026-08-29.

## Announcement

2026-08-22 19:45:38, block 963,629, `b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77`, 5,000 sats to the escrow:

> I made a Bitcoin puzzle using information contained in the genesis block created by Satoshi to generate the wallet.
>
> The entropy is extremely low. I didn't even need to back anything up. Everything I needed was already in the genesis block.
>
> Good luck!

The escrow had been funded with 20,000 sats 17 hours earlier
(`e2aaa928a965ee02b9c9a76227383113a62f350701a18d7792372712ce501ac7`, block 963,517,
2026-08-22 02:45:22, no message).

## Hint channel

2026-08-23 01:51:20, block 963,659, `248f690de194372564baa14e1bebf08154e2f2042ed205baa6157fdc0e3f22ea`, 5,000 sats:

> If you have a question, you can include it with a transaction sent directly to this address, and I will reply with a hint.
>
> Larger payments receive better hints. Dust transactions will be ignored.

## Questions and answers

| Time | Block | Txid | From | To escrow | Text |
|---|---|---|---|---|---|
| 2026-08-23 14:41:38 | 963,739 | `3b2f8aef7bb8f56dc939b34465906fd8a7693b2c8718d541ea635f8780313db6` | player 1 | 12,916 sats | Is the witness script a hash lock, a multisig, or something else? |
| 2026-08-23 15:43:56 | 963,744 | `0fb7a2f175dd7f9b8826cf2923ce4fcb56e4c7bfe252903e6dad1f87f177dfe3` | author | 12,916 sats | The witness script is a multisig. |
| 2026-08-23 18:19:26 | 963,758 | `268093b9ae56a59d2bb1a6acde588d6763fe859947b098c235031493208d3e22` | author (relayed, player 1) | 16,028 sats | How many keys, what threshold, and how are the keys derived from genesis? |
| 2026-08-23 21:08:58 | 963,768 | `ef63243d374d8eabeac7e17e06cc4b1b672146dc61a8e5180eeac980cec07302` | author | 16,028 sats | Two keys, both required. The rest is for you to derive. |
| 2026-08-24 06:40:09 | 963,823 | `fe27df994d658e79bea7b4cfe2427341ce024c70c5af21b76186807eebe57072` | author (relayed, player 1) | 6,345 sats | Are both keys from the same genesis field, and is the function a hash? |
| 2026-08-24 07:13:18 | 963,829 | `82a076b02643372769ac676d260ef4d9854c6bf49370ed61875fc63b8241dcfc` | author | 2,000 sats | Yes, both keys use the same Genesis field, and there is no hash. |
| 2026-08-24 08:58:20 | 963,837 | `2f5bbc7c0d031f54c9b7c8bee73eb2607d04b19019d1deac7f773eafdd1b91f8` | author (relayed, player 1) | 12,843 sats | Is the second key derived from the first, or both from genesis independently? |
| 2026-08-24 14:32:47 | 963,868 | `ff884832e937f972c92c012ba235ff45b549cd1702dfd02691056da6bc1ff913` | author | 2,000 sats | Both keys are derived independently from Genesis. |
| 2026-08-24 18:01:41 | 963,888 | `69d19cc41b8a5f1e711d46069e301bb4d29223bfcf1128eb6a9236e0d3e9b96c` | player 1 | 12,703 sats | Which genesis field, hash, merkle, nonce, time, headline, or pubkey? |
| 2026-08-24 21:35:20 | 963,910 | `eb609dfede7f61d3bf9fe79ae48e546c358ebd09c05b3cd64a22433cb784ea86` | author | 2,000 sats | The Genesis Block is public. Which part of it matters is for you to discover. |
| 2026-08-28 17:38:24 | 964,465 | `51b9f9521ca5bfae851b0f55dc3b151914b95f77eef156078a422396cd30cef2` | player 2 | 2,000 sats | Prize Address?Genesis field 32 bytes or smaller? |
| 2026-08-28 20:15:31 | 964,477 | `84fc5defe22590a02bbe0025831be110ed6f9e0bc53c3c835a4e42479b0bf050` | player 2 | 3,000 sats | Give a hint at your will! |
| 2026-08-28 22:45:35 | 964,486 | `610fc4d2ca1a214d99248c8188fd2973f4c51fca319ccf9ab983ac3edf4b1821` | player 2 | 3,500 sats | Can you give any hint about derivation offset/rule? |
| 2026-08-28 23:15:28 | 964,491 | `6e94cfcbc1350a138242f97310dfd0280371a0020380cb32b2512337470c1077` | author | 5,000 sats | Solve it to find out. Maybe both. (newline) If you can't check the Genesis block, you can also use The Times newspaper! |
| 2026-08-28 23:50:52 | 964,496 | `8be479605bc8f2facd2036fd1b7f5cfa3a3f3920eeffee75e0004a2cff4d25d6` | author | 3,500 sats | `Derivation rule: root -> multisig -> mainnet -> genesis_data -> script_type` |
| 2026-09-06 15:51:27 | 965,798 | `68e79190221d2b73089b523f7f5af2a11838339a788239f4eee30d6c1d4502e7` | player 3 | 1,000 sats | give another hint |
| 2026-09-06 19:41:00 | 965,824 | `64385a0cc5c4c712d1d9d8628e1e00364310d9ba50536ccd23c71b49ae66b96b` | author | 1,000 sats | I can't give hints without a question. Low-value transactions get bad hints; dust will be ignored. |
| 2026-09-10 20:47:36 | 966,402 | `75daa8e824abba4fe1b1a4b12f923b50291fab98743edaa1f03ef8c50bb70552` | player 4 | 10,000 sats | Root = Times text as BIP32 seed? BIP39? raw key? genesis_data = BIP48 account? |
| 2026-09-10 21:33:46 | 966,409 | `cb47c7a73c1aaa11bfe0edce41c2ef7c9c1fec1478efd15e40b226eb502dcc18` | author | 2,000 sats | root = the master key derived from the BIP39 seed; genesis_data = some data from the genesis block used as the BIP48 account number. |
| 2026-09-11 21:25:51 | 966,565 | `6497aef4be0d5be68644296d5fcdb709c66bb20db5972f4e53f90836e27862fe` | player 4 | 10,000 sats | BIP39 entropy: genesis bytes/puzzle text/img/other? words 12/24? passphrase Y/N? |
| 2026-09-11 23:26:17 | 966,576 | `f8f04fc04e2c4f34dc2264f85ff7944c6aa822446bc4cc082e95a52aed5c2a4c` | author | 2,000 sats | BIP39: 12 words; Passphrase: Y; Entropy: The data needed to solve it is publicly available in the genesis block. |
| 2026-09-14 13:01 | 966,966 | `e43647274f672f9b4eb42fff1d15f2afcaa8bfd4650823403a18a76774999169` | player 5 | 10,000 sats | Passphrase: genesis data or your own word? How long? What built the wallet? |
| 2026-09-14 16:15 | 966,989 | `a137a898ab56180d6e9ebac602377a120511acdec0b4ebe4e806536652d3b32d` | author | 2,000 sats | Passphrase: Who received the first transaction? That's all I've got to say. What built the wallet are the tools that support BIPs 32, 39, and 48. |
| 2026-09-15 01:30 | 967,051 | `af08a3d048ac44c5888767890532c68b5004e44a2025daf0cbbbb8281a6ee9d9` | player 6 | 4,500 sats | Passphrase sha256 first 8 hex? Entropy: raw 16B slice of Times or sha256? |
| 2026-09-15 03:19 | 967,064 | `a3878ff0c813a726c755e5b1220b69dc3528989fea1095041a8edadefc269fc4` | author | 2,000 sats | No, the passphrase is a name. The entropy isn't the raw 16 bytes. |
| 2026-09-15 09:34 | 967,106 | `b073a2ef7a9a51e8431d48315bfe9f1804a34f5169cae4678af9d92a03860a7b` | player 5 | 10,000 sats | Do both cosigners use the same 12 words and the same passphrase? |
| 2026-09-15 14:31 | 967,135 | `fafdcd55a566ccebe3944b3a4cb3d4d04ced285a4b9aa3da0ccd2279eee57dad` | player 5 | 5,000 sats | Were the 12 words generated from entropy, or chosen directly as words? |
| 2026-09-15 15:22 | 967,140 | `96861335409aa5dd85cc03734191832dfb5e5ff1476d4005ccdb69c286217fcf` | author | 1,784 sats | Perhaps... but figuring that out is part of the puzzle. The 12 words were generated from entropy. |
| 2026-09-16 09:02 | 967,260 | `de3c7aba7b3b8d3650c339041579158125546ff9d3bcfeef02fefe489a73e4d0` | player 5 | 5,000 sats | Is the 128-bit entropy a zero-padded number, a digest, or neither? |
| 2026-09-16 12:40 | 967,281 | `e38caf86a0d304a4d8a10e023e75626387dbce287847d46076a48bf60be82ca2` | author | 1,848 sats | It's a 128-bit digest. |
| 2026-09-17 07:34 | 967,379 | `530490fd94eb76e368a0eff96db87cb1bb74ac1027aa97765a34508d877c4de4` | player 5 | 4,000 sats | Passphrase fmt: first/full/middle name? spaced/joined? lower/UPPER/Capitalized? |
| 2026-09-17 08:02 | 967,383 | `ec08d0014b545776344e84214c82d556e25f11eb91f5764fc2b5b3b18faf4c99` | author | 1,813 sats | Passphrase: You'll have to discover the fmt through brute force. The key question greatly narrows the search space. |
| 2026-09-17 10:44 | 967,396 | `a347081cb74dd40f1a7cbe4a5dcb6f8f8a79d526cd07141c80a85e6ab6eec26e` | player 5 | 3,000 sats | Digest input: typed text, raw block bytes, a file, or something else? |
| 2026-09-17 23:22 | 967,477 | `ed010443963e3601b35266a52108bd1b8dfa58e9e258a041098c05a474513fab` | author | 1,777 sats | The genesis block data can be viewed in binary, hex, decimal, or ASCII. If you figure out which part is being used as the entropy, just try all four forms. (newline) Want a valuable hint? Send 50k sats and I'll reveal the public keys for this address. |

The three relayed questions were first paid by player 1 directly to the author's change
address of the moment, off the escrow's history: 32,357 sats on 2026-08-23 16:20:06
(`d271c37d8ce26247`), 6,465 sats on 2026-08-23 19:37:09 (`a2209eef7490846b`), 12,963 sats on
2026-08-24 03:35:54 (`f6579e67ff234ddb`). Player 1 also paid its first question twice, once
to the author (12,909 sats, `1b4bde84af7df419`, 14:34:56) and once to the escrow.


Player 4's two questions (2026-09-10 and 2026-09-11, 10,000 sats each) are, word for word, the
draft questions written in this folder's `analysis/leads.md` on 2026-08-29. I did not send them;
a reader did, and the author answered both within the hour.


The 2026-09-14 to 2026-09-17 exchange is attributed from the transaction inputs. The author
spends a chain of P2WPKH change outputs, one per message:
`bc1qw720l9e6g4a675vfraghzm93gvyw8s2fjgtdxy` to `bc1qv7ezkqngwaeutstj8prd9wjk7w26j44sxxljry`
to `bc1qqenp579zef3fpetekf424w9hk6eadlz0lpmtja` to `bc1q6suweqz66uwhnpedulfwkmvn8lu06elyftzytq`
to `bc1q5eg4w0ewlhvm92kv694v5slldy62kjjpzzyewm` to `bc1qnsk37lnc9unj4d4jjq5j3nh5u88dvfltv9r7xr`,
which is the author's current change output and is unspent at 2026-09-17 15:30 UTC. Player 5
spends a chain of P2TR outputs starting at `bc1qdu8mh9qjtjhy89mvhmcgf66ul6ld92rdr6qzad` and
has 34,970 sats left in `bc1prp6jmy2u5qy28u6z9jzfevpr4lv4sv2dzuvkzsv38apa8nznd70q0snce5`.
Player 6 appears once, from `bc1qcw0yf68uxk0pj3p3fuepvsujevfy0uzwaul4vq`.

The 2026-09-15 15:22 answer covers the two questions player 5 had sent before it: "Perhaps"
answers whether both cosigners share the 12 words and the passphrase, and the second clause
answers whether the words were generated from entropy.

The author's reply to player 5's 3,000-sat question was sent twice. The first version,
`5659ab70213e2e5b6811cdecf421e158d810617d765fa725ff80f20e0b9684fb`, paid 58 sats of fee, sat
unconfirmed for about seven hours, and carried only a link to the "I don't know, my memory ain't
so great" scene from The Naked Gun (1988). The author then replaced it by fee substitution with
`ed010443963e...`, 136 sats of fee, which confirmed in block 967,477 and carries the hint above.
The replaced transaction no longer exists in any mempool and is recorded here only because its
first version is what a reader watching the channel that afternoon would have seen. Both spend
the same change output `bc1qnsk37lnc9unj4d4jjq5j3nh5u88dvfltv9r7xr`, which attributes them to
the author.

The confirmed message is the first statement about how the entropy input is written rather than
about which part it is, and it prices a further hint: 50,000 sats for the escrow's two public
keys.
