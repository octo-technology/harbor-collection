from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 12, 5, 11, 29, 00),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(hours=1)
}

dag = DAG(
    'test-rre',
    default_args=default_args,
    schedule_interval=timedelta(hours=1)
)

#run_this = BashOperator(
#    task_id='run_after_loop',
#    bash_command='echo 1',
#    dag=dag,
#)

k8s = KubernetesPodOperator(
    namespace='default',
    image="aquasec/kube-bench:latest",
    cmds=["kube-bench", "--json", "--logtostderr"],
    labels={"app": "kube-bench"},
    name="kube-bench",
    task_id="kube-bench",
    volumes=[
        Volume(name="var-lib-etcd", configs={'hostPath': {"path": "/var/lib/etcd"}}),
        Volume(name="var-lib-kubelet", configs={'hostPath': {"path": "/var/lib/kubelet"}}),
        Volume(name="etc-systemd", configs={'hostPath': {"path": "/etc/systemd"}}),
        Volume(name="etc-kubernetes", configs={'hostPath': {"path": "/etc/kubernetes"}}),
        Volume(name="usr-bin", configs={'hostPath': {"path": "/usr/bin"}}),
    ],
    volume_mounts=[
        VolumeMount('var-lib-etcd', mount_path='/var/lib/etcd', sub_path=None, read_only=True),
        VolumeMount('var-lib-kubelet', mount_path='/var/lib/kubelet', sub_path=None, read_only=True),
        VolumeMount('etc-systemd', mount_path='/etc/systemd', sub_path=None, read_only=True),
        VolumeMount('etc-kubernetes', mount_path='/etc/kubernetes', sub_path=None, read_only=True),
        VolumeMount('usr-bin', mount_path='/usr/bin', sub_path=None, read_only=True),
    ],
    get_logs=True,
    in_cluster=True,
    is_delete_operator_pod=True,
    dag=dag
)

k8s.set_upstream(start)
