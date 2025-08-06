package edu.wgu.d387_sample_code;

import edu.wgu.d387_sample_code.Reader.ReaderResource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

@RestController
@RequestMapping("/resources")
@CrossOrigin
public class ResourcesController {

    // Create 2 executors
    private Executor ex = Executors.newFixedThreadPool(2);

    @GetMapping("/welcome")
    public ResponseEntity<List<String>>getMsg() {
        List<String> l = new ArrayList<String>();

        // Read en_US
        try {
            ex.execute(() -> {
                ReaderResource rrEN = new ReaderResource("en", "US");
                System.out.println("en starting....");
                l.add(rrEN.getMsg());
                System.out.println("en received");
            });
        } catch (Exception e) {
            e.printStackTrace();
        }

        ex.execute(() -> {
            ReaderResource rrFR = new ReaderResource("fr", "CA");
            System.out.println("fr starting....");
            l.add(rrFR.getMsg());
            System.out.println("fr received");
        });

        return ResponseEntity.ok(l);

    }
}

