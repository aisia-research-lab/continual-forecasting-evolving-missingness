"""Inspect archival release traces for strict time ordering (schema-aware)."""
import argparse,tarfile,json,collections

def audit(archive):
    total=0;fail=[];skipped=collections.Counter()
    with tarfile.open(archive,'r:gz') as t:
        for item in t:
            if not item.isfile() or not item.name.endswith('/release_trace.jsonl') or 'smoke' in item.name:continue
            f=t.extractfile(item)
            for ln,line in enumerate(f,1):
                if not line.strip():continue
                event=json.loads(line);total+=1
                # Different historical runners use different naming conventions.
                if 'release_time' in event and 'used_at' in event:
                    if not float(event['release_time'])<float(event['used_at']):fail.append((item.name,ln,'release_time'))
                elif 'target_end' in event and 'delay' in event and 'used_at' in event:
                    if not float(event['target_end'])+float(event['delay'])<float(event['used_at']):fail.append((item.name,ln,'target_end+delay'))
                else:skipped[','.join(sorted(event.keys()))]+=1
    print('events=',total,'violations=',len(fail),'unchecked_schema_events=',sum(skipped.values()))
    if skipped: print('WARNING unsupported event schemas:',skipped.most_common(2))
    if fail:print(fail[:10]);raise SystemExit(1)
    if skipped:raise SystemExit(2)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',required=True)
    audit(p.parse_args().archive)
