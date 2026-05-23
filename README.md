# TenSEAL Basics (CKKS Homomorphic Encryption Demo)

This repository demonstrates a basic workflow of **Fully Homomorphic Encryption (FHE)** using the **TenSEAL library (CKKS scheme)** in Python.

It shows how encrypted data can be:
- Created using a secret key
- Converted into a public-only computation context
- Processed (addition + multiplication) without decryption
- Finally decrypted to verify correctness

---

##  Credit

This project is based on the tutorial:

 https://www.youtube.com/watch?v=2qkCLaeD7pA

All core concepts and code structure are inspired by the above video, with some modifications and reorganizations made for learning and experimentation purposes.

---

##  Concept Overview

We use **CKKS (Cheon–Kim–Kim–Song)** encryption, which allows approximate arithmetic on encrypted data. This is useful for privacy-preserving computations like:

- Encrypted financial calculations
- Secure machine learning inference
- Private cloud computation

---

## 📁 Project Structure

```

.
├── owner.ipynb        # Key generation + encryption + decryption (trusted side)
├── operator.ipynb     # Performs encrypted computation (untrusted side)
├── utils.py           # Helper functions for file read/write
├── requirements.txt   # Dependencies
├── .gitignore
├── keys/
│   ├── secret.txt     # Full context (includes secret key)
│   └── public.txt     # Public computation context only
├── outputs/
│   ├── salary_enc.txt
│   └── bonus_enc.txt
│   └── salary_enc_new.txt (generated after computation)

````

---

##  Workflow Explanation

### 1. Key Generation (Owner Side)

In `owner.ipynb`:

- A CKKS encryption context is created
- Galois keys are generated for advanced operations
- Global scale is set for precision control

```python
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
context.generate_galois_keys()
context.global_scale = 2**40
````

* The full context (including secret key) is saved as:

```
keys/secret.txt
```

* Then the secret key is removed:

```python
context.make_context_public()
```

* Public context is saved:

```
keys/public.txt
```

---

### 2. Encryption (Owner Side)

The owner encrypts sensitive data:

```python
salary = [10000]
bonus = [600]

salary_enc = ts.ckks_vector(context, salary)
bonus_enc = ts.ckks_vector(context, bonus)
```

These encrypted values are stored in:

```
outputs/salary_enc.txt
outputs/bonus_enc.txt
```

---

### 3. Encrypted Computation (Operator Side)

In `operator.ipynb`, only the **public context** is used:

```python
context = ts.context_from(utils.read_data("keys/public.txt"))
```

Encrypted values are loaded in a *lazy form*:

```python
salary_enc = ts.lazy_ckks_vector_from(salary_proto)
salary_enc.link_context(context)
```

Same for bonus.

Then computation is performed directly on encrypted data:

```python
wage_increase_rate_plain = ts.plain_tensor([1.2])

salary_new_enc = (salary_enc * wage_increase_rate_plain) + bonus_enc
```

###  Important Note:

* Data remains encrypted throughout computation
* Operator never accesses raw salary or bonus values

---

### 4. Decryption (Owner Side Only)

After computation, the result is decrypted using the secret context:

```python
m = ts.lazy_ckks_vector_from(m_proto)
m.link_context(context)

print(round(m.decrypt()[0], 2))
```

Expected output:

```
12600.0
```

---

## ⚙️ Key Features Demonstrated

* CKKS homomorphic encryption
* Public/private context separation
* Encrypted arithmetic (multiply + add)
* Lazy loading of encrypted vectors
* Secure computation model (cloud-style workflow)

---

##  Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

Main dependency:

* `tenseal`

---

##  Learning Outcome

This project helps understand:

* How encrypted data can still be computed on
* Separation of trust between data owner and computation server
* Real-world FHE workflow patterns

---



