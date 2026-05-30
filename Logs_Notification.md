# Log & Progress Notifications - Complete Walkthrough

---

## Pehle problem samjho

Maan lo tumhara tool **2 minute** leta hai complete hone mein.

```
User: "convert this 4GB video"
          ↓
      [2 minute silence...]
          ↓
User sochta hai:
"Kya crash ho gaya? 
 Kya tool chala bhi?
 Main dobara run karun?"
```

**Yeh bad UX hai.** Notifications isi problem ka solution hain.

---

## Notifications kya hain?

Server tool chala raha hota hai — beech beech mein **client ko update bhejta rehta hai:**

```
"10% ho gaya..."
"file read ho gayi..."
"50% ho gaya..."
"almost done..."
"complete!"
```

Yeh do tarah ke hote hain:

| Type                            | Kaam                    | Example             |
| ------------------------------- | ----------------------- | ------------------- |
| **Log Notification**      | Text message bhejo      | "File read ho gayi" |
| **Progress Notification** | Percentage update bhejo | 45/100              |

---

## Architecture - Kaun kisko bhejta hai?

Sampling ki tarah yahan bhi **Server → Client** direction hai:

```
Normal tool call:
Client  →→→  Server   (client ne tool chalaya)

Notifications:
Server  →→→  Client   (server beech mein updates bhej raha hai)
```

---

## Dry Run - Video Converter Tool

### Setup - Server Side

```python
# Server pe tool kuch aisa hoga
async def convert_video(file_path, context):  
    #                            ↑
    #                    yeh context argument
    #                    automatically aata hai
    #                    isi se notifications bhejte hain

    # Step 1 - log notification
    await context.info("File reading start ho rahi hai...")
    video = read_file(file_path)

    # Step 2 - progress notification
    await context.report_progress(25, 100)  # 25%

    # Step 3 - processing
    await context.info("Conversion chal rahi hai...")
    result = convert(video)

    # Step 4 - progress
    await context.report_progress(75, 100)  # 75%

    # Step 5 - done
    await context.report_progress(100, 100)
    await context.info("Complete!")

    return result
```

**`context` object do cheezein deta hai:**

* `context.info()` → log message bhejo
* `context.report_progress()` → progress update bhejo

---

### Setup - Client Side

```python
# Client pe do callbacks banao

# Callback 1 - logs ke liye
def on_log(message):
    print(f"[LOG]: {message}")
    # ya UI mein show karo
    # ya file mein save karo
    # tumhari marzi

# Callback 2 - progress ke liye  
def on_progress(current, total):
    percent = (current/total) * 100
    print(f"[PROGRESS]: {percent}%")
    # ya progress bar update karo

# Yeh callbacks pass karo
session = ClientSession(log_callback=on_log)

result = await session.call_tool(
    "convert_video",
    progress_callback=on_progress  # yahan pass karo
)
```

---

## Poora Flow - Dry Run

```
User: "convert bigfile.mp4"
          ↓

CLIENT
  |
  |---[call_tool: convert_video]---->  SERVER
                                          |
                                          | context.info("File reading...")
                                          |
  [log notification] <------------------  |
  on_log() chala → "[LOG]: File reading..."
  (user ko dikha)
                                          |
                                          | context.report_progress(25, 100)
                                          |
  [progress notification] <-------------  |
  on_progress() chala → "[PROGRESS]: 25%"
  (progress bar update)
                                          |
                                          | context.info("Conversion chal rahi...")
                                          |
  [log notification] <------------------  |
  "[LOG]: Conversion chal rahi..."
                                          |
                                          | context.report_progress(75, 100)
                                          |
  [progress notification] <-------------  |
  "[PROGRESS]: 75%"
                                          |
                                          | context.report_progress(100, 100)
                                          | context.info("Complete!")
                                          |
  [notifications] <--------------------   |
  "[PROGRESS]: 100%"
  "[LOG]: Complete!"
                                          |
  [FINAL RESULT] <---------------------   |
  "converted_bigfile.mp4"
          ↓
       User ko dikh raha hai sab kuch real-time
```

---

## Sampling vs Notifications - Farq

Yahan ek important farq samjho:

```
SAMPLING:
Server → Client → "tu LLM call kar mujhe result chahiye"
Client kuch kaam karta hai phir result wapas bhejta hai
Yeh ek REQUEST hai — response expect hota hai

NOTIFICATIONS:
Server → Client → "yeh update sun le"
Client sirf display karta hai, koi kaam nahi karta
Yeh sirf ek EVENT hai — koi response nahi chahiye
```

---

## Key Points

**Server side pe:**

* Tool function mein `context` last parameter hota hai — automatically milta hai
* `context.info()` — log bhejo
* `context.report_progress(current, total)` — progress bhejo

**Client side pe:**

* Log ke liye alag callback
* Progress ke liye alag callback
* Dono optional hain — na banao toh bhi tool chalega, bas updates nahi dikhenge

**Overall:**

> Notifications **optional** hain — sirf UX better karne ke liye hain. Inka tool ke actual kaam se koi lena dena nahi. Agar remove kar do toh tool waise hi kaam karega, bas user ko pata nahi chalega andar kya ho raha hai.






>
> # Step 2 - progress notification await context.report_progress(25, 100) # 25%
>
> mtlb





## `report_progress(25, 100)` ka matlab

---

```python
context.report_progress(25, 100)
#                        ↑   ↑
#                     current total
```

Bas itna hi hai:

```
"100 mein se 25 kaam ho gaya"
= 25%
```

---

## Dry Run

```python
context.report_progress(0, 100)    # shuru hua    → 0%
context.report_progress(25, 100)   # thoda hua    → 25%
context.report_progress(50, 100)   # adha hua     → 50%
context.report_progress(75, 100)   # zyada hua    → 75%
context.report_progress(100, 100)  # complete     → 100%
```

---

## Total 100 hi kyun?

100 hona **zaruri nahi.** Yeh tumhari marzi hai:

```python
# Agar 4 files process kar rahe ho
context.report_progress(1, 4)   # 1 file done
context.report_progress(2, 4)   # 2 files done
context.report_progress(3, 4)   # 3 files done
context.report_progress(4, 4)   # sab done

# Client khud calculate karega:
# 1/4 = 25%
# 2/4 = 50%  
# etc.
```

> **Current aur Total** — bas yeh do numbers bhejte ho. Client inhe le ke jo chahe display kare, progress bar banaye ya percentage dikhaye.
>
