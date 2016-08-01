configfile: "config2.json"
rule fastq2fasta:
    input: '{prefix}/{sample}.fastq'
    output:'{prefix}/{sample}.fasta'
    message: """---Converting fastq to fasta."""
    shell : "perl ../bin/fq2fa.pl -i {input} -o {output}"
rule bowtie2_map:
    input:
       ref=config["reference"],
       reads=rules.fastq2fasta.output
    output:
       index= '{prefix}/{sample}.assembly.out/{sample}.index',
       pref='{prefix}/{sample}.assembly.out/{sample}.index',
       sam= '{prefix}/{sample}.assembly.out/{sample}.sam'
    log: '{prefix}/{sample}.step2.log'
    threads:config["nthreads"]
    message: """---Build index ."""
    shell:"bowtie2-build --threads {threads} -q {input.ref} {output.pref} 1>> {output.index} 2>&1;bowtie2 --end-to-end -D 15 -R 2 -N 0 -L 31 -i S,1,1.15 -p {threads} -x {output.pref} -f {input.reads} -S {output.sam} > {log} 2>&1"