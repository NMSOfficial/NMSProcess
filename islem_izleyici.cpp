#include "islem_izleyici.h"
#include <QProcess>
#include <QOperatingSystemVersion>

IslemIzleyici::IslemIzleyici(QObject *ebeveyn)
    : QObject(ebeveyn), izlenenIslem("") {
    izlemeZamani.setInterval(1000); // 1 saniye aralıklarla izleme
    connect(&izlemeZamani, &QTimer::timeout, this, &IslemIzleyici::islemIzle);
}

void IslemIzleyici::izlemeyiBaslat(const QString &islem) {
    izlenenIslem = islem;
    izlemeZamani.start();
    emit logGuncellendi("İzleme başlatıldı: " + islem);
}

void IslemIzleyici::izlemeyiDurdur() {
    izlemeZamani.stop();
    emit logGuncellendi("İzleme durduruldu: " + izlenenIslem);
}

void IslemIzleyici::islemIzle() {
    QProcess process;
    QString command;
    QStringList arguments;

#if defined(Q_OS_WIN)
    command = "tasklist /v /fo csv";
#elif defined(Q_OS_MAC)
    command = "ps";
    arguments << "-eo" << "pid,comm,pcpu,pmem";
#else
    command = "ps";
    arguments << "-eo" << "pid,comm,%cpu,%mem";
#endif

    process.start(command, arguments);
    process.waitForFinished();
    QString output = process.readAllStandardOutput();

    QStringList lines = output.split('\n');
    foreach (const QString &line, lines) {
        if (line.contains(izlenenIslem)) {
            emit logGuncellendi(line);
        }
    }
}

