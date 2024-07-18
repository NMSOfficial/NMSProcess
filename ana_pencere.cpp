#include "ana_pencere.h"
#include <QVBoxLayout>
#include <QFileDialog>
#include <QMessageBox>
#include <QProcess>
#include <QOperatingSystemVersion>

AnaPencere::AnaPencere(QWidget *ebeveyn)
    : QMainWindow(ebeveyn), islemIzleyici(new IslemIzleyici(this)) {
    logoEtiketi = new QLabel(this);
    QPixmap logo(":/logo.png");
    logoEtiketi->setPixmap(logo.scaled(200, 200, Qt::KeepAspectRatio));

    islemComboBox = new QComboBox(this);

    baslatDugmesi = new QPushButton("İzlemeyi Başlat", this);
    durdurDugmesi = new QPushButton("İzlemeyi Durdur", this);
    kaydetDugmesi = new QPushButton("Logu Kaydet", this);
    filtreleDugmesi = new QPushButton("Logu Filtrele", this);
    araDugmesi = new QPushButton("Logda Ara", this);
    logMetinEdit = new QTextEdit(this);
    filtreGirdi = new QLineEdit(this);
    araGirdi = new QLineEdit(this);

    QVBoxLayout *dikeyYerlesim = new QVBoxLayout;
    dikeyYerlesim->addWidget(logoEtiketi);
    dikeyYerlesim->addWidget(islemComboBox);
    dikeyYerlesim->addWidget(baslatDugmesi);
    dikeyYerlesim->addWidget(durdurDugmesi);
    dikeyYerlesim->addWidget(kaydetDugmesi);
    dikeyYerlesim->addWidget(filtreGirdi);
    dikeyYerlesim->addWidget(filtreleDugmesi);
    dikeyYerlesim->addWidget(araGirdi);
    dikeyYerlesim->addWidget(araDugmesi);
    dikeyYerlesim->addWidget(logMetinEdit);

    QWidget *merkezWidget = new QWidget(this);
    merkezWidget->setLayout(dikeyYerlesim);
    setCentralWidget(merkezWidget);

    connect(baslatDugmesi, &QPushButton::clicked, this, &AnaPencere::izleBaslat);
    connect(durdurDugmesi, &QPushButton::clicked, this, &AnaPencere::izleDurdur);
    connect(kaydetDugmesi, &QPushButton::clicked, this, &AnaPencere::logKaydet);
    connect(filtreleDugmesi, &QPushButton::clicked, this, &AnaPencere::logFiltrele);
    connect(araDugmesi, &QPushButton::clicked, this, &AnaPencere::logAra);
    connect(islemIzleyici, &IslemIzleyici::logGuncellendi, this, [this](const QString &log) {
        logMetinEdit->append(log);
        logVeri += log + "\n";
    });

    // İşlem listesini yükleyin
    islemleriYukle();
}

AnaPencere::~AnaPencere() {}

void AnaPencere::izleBaslat() {
    QString islem = islemComboBox->currentText();
    if (!islem.isEmpty()) {
        islemIzleyici->izlemeyiBaslat(islem);
    }
}

void AnaPencere::izleDurdur() {
    islemIzleyici->izlemeyiDurdur();
}

void AnaPencere::logKaydet() {
    QString dosyaAdi = QFileDialog::getSaveFileName(this, "Logu Kaydet", "", "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)");
    if (!dosyaAdi.isEmpty()) {
        QFile dosya(dosyaAdi);
        if (dosya.open(QIODevice::WriteOnly | QIODevice::Text)) {
            QTextStream out(&dosya);
            out << logMetinEdit->toPlainText();
            dosya.close();
        } else {
            QMessageBox::warning(this, "Hata", "Log dosyasını kaydedemedi");
        }
    }
}

void AnaPencere::islemleriYukle() {
    QProcess process;
    QStringList arguments;
    QString command;

#if defined(Q_OS_WIN)
    command = "tasklist";
#elif defined(Q_OS_MAC)
    command = "ps";
    arguments << "-e";
#else
    command = "ps";
    arguments << "-e";
#endif

    process.start(command, arguments);
    process.waitForFinished();
    QString output = process.readAllStandardOutput();

    QStringList lines = output.split('\n');
    foreach (const QString &line, lines) {
#if defined(Q_OS_WIN)
        if (line.contains(".exe")) {
            QStringList parts = line.split(QRegExp("\\s+"), QString::SkipEmptyParts);
            if (!parts.isEmpty()) {
                islemComboBox->addItem(parts.first());
            }
        }
#else
        QStringList parts = line.split(QRegExp("\\s+"), QString::SkipEmptyParts);
        if (parts.size() > 3) {
            islemComboBox->addItem(parts.last());
        }
#endif
    }
}

void AnaPencere::logFiltrele() {
    QString filtre = filtreGirdi->text();
    QStringList logSatirlari = logVeri.split('\n');
    logMetinEdit->clear();
    foreach (const QString &satir, logSatirlari) {
        if (satir.contains(filtre, Qt::CaseInsensitive)) {
            logMetinEdit->append(satir);
        }
    }
}

void AnaPencere::logAra() {
    QString ara = araGirdi->text();
    QStringList logSatirlari = logVeri.split('\n');
    logMetinEdit->clear();
    foreach (const QString &satir, logSatirlari) {
        if (satir.contains(ara, Qt::CaseInsensitive)) {
            logMetinEdit->append(satir);
        }
    }
}

